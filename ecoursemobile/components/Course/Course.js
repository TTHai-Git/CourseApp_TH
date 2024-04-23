import moment from "moment";
import React from "react";
import { ActivityIndicator, Image, ScrollView, View } from "react-native";
import { Chip, List, Searchbar } from "react-native-paper";
import APIS, { endpoints } from "../../configs/APIS";
import MyStyles from "../../configs/styles/MyStyles";
import "moment/locale/vi";

const Course = () => {
  const [categories, setCategories] = React.useState(null);
  const [courses, setCourses] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [q, setQ] = React.useState("");
  const [cateId, setCateId] = React.useState("");

  const loadCates = async () => {
    try {
      let res = await APIS.get(endpoints["categories"]);
      setCategories(res.data);
    } catch (ex) {
      console.error(ex);
    }
  };

  const loadCourse = async () => {
    try {
      let url = `${endpoints["courses"]}?q=${q}&category_id=${cateId}`;
      let res = await APIS.get(url);
      setCourses(res.data.results);
      setLoading(false);
    } catch (ex) {
      console.error(ex);
    }
  };

  React.useEffect(() => {
    loadCates();
  }, []);

  React.useEffect(() => {
    loadCourse();
  }, [q, cateId]);

  return (
    <View style={MyStyles.container}>
      <View style={MyStyles.row}>
        {categories === null ? (
          <ActivityIndicator />
        ) : (
          <>
            {categories.map((c) => (
              <Chip
                style={MyStyles.margin}
                key={c.id}
                mode={c.id === cateId ? "outlined" : "flat"}
                icon="shape-outline"
                onPress={() => setCateId(c.id)}
              >
                {c.name}
              </Chip>
            ))}
            <Chip
              style={MyStyles.margin}
              mode={!cateId ? "outlined" : "flat"}
              icon="shape-outline"
              onPress={() => setCateId("")}
            >
              Show All
            </Chip>
          </>
        )}
      </View>

      <Searchbar placeholder="Search" onChangeText={setQ} value={q}></Searchbar>

      <ScrollView>
        {courses.map((c) => (
          <List.Item
            style={MyStyles.margin}
            key={c.id}
            title={c.subject}
            description={moment(c.created_date).fromNow()}
            left={() => (
              <Image style={MyStyles.avatar} source={{ uri: c.image }} />
            )}
          />
        ))}
        {loading && <ActivityIndicator />}
      </ScrollView>
    </View>
  );
};
export default Course;

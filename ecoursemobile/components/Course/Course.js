import moment from "moment";
import React from "react";
import {
  ActivityIndicator,
  Image,
  RefreshControl,
  ScrollView,
  TouchableOpacity,
  View,
} from "react-native";
import { Chip, List, Searchbar } from "react-native-paper";
import APIS, { endpoints } from "../../configs/APIS";
import MyStyles from "../../configs/styles/MyStyles";
import "moment/locale/vi";
import Item from "../Utils/item";
import isCloseToBottom from "../Utils/utils";

const Course = ({ navigation }) => {
  const [categories, setCategories] = React.useState(null);
  const [courses, setCourses] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [q, setQ] = React.useState("");
  const [cateId, setCateId] = React.useState("");
  const [page, setPage] = React.useState(1);

  const loadCates = async () => {
    try {
      let res = await APIS.get(endpoints["categories"]);
      setCategories(res.data);
    } catch (ex) {
      console.error(ex);
    }
  };

  const loadCourse = async () => {
    if (page > 0) {
      try {
        setLoading(true);
        let url = `${endpoints["courses"]}?q=${q}&category_id=${cateId}&page=${page}`;
        let res = await APIS.get(url);
        if (page === 1) setCourses(res.data.results);
        else if (page > 1)
          setCourses((current) => {
            return [...current, ...res.data.results];
          });
        if (res.data.next === null) setPage(0);
      } catch (ex) {
        console.error(ex);
      } finally {
        setLoading(false);
      }
    }
  };

  React.useEffect(() => {
    loadCates();
  }, []);

  React.useEffect(() => {
    loadCourse();
  }, [q, cateId, page]);

  // const isCloseToBottom = ({
  //   layoutMeasurement,
  //   contentOffset,
  //   contentSize,
  // }) => {
  //   const paddingToBottom = 20;
  //   return (
  //     layoutMeasurement.height + contentOffset.y >=
  //     contentSize.height - paddingToBottom
  //   );
  // };

  const loadMore = ({ nativeEvent }) => {
    if (loading === false && isCloseToBottom(nativeEvent)) {
      setPage(page + 1);
    }
  };

  const search = (value, callback) => {
    setPage(1);
    callback(value);
  };

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
                onPress={() => search(c.id, setCateId)}
              >
                {c.name}
              </Chip>
            ))}
            <Chip
              style={MyStyles.margin}
              mode={!cateId ? "outlined" : "flat"}
              icon="shape-outline"
              onPress={() => search("", setCateId)}
            >
              Show All
            </Chip>
          </>
        )}
      </View>

      <Searchbar
        placeholder="Search"
        onChangeText={(t) => search(t, setQ)}
        value={q}
      ></Searchbar>

      <ScrollView onScroll={loadMore}>
        <RefreshControl onRefresh={() => loadCourse} />
        {loading && <ActivityIndicator />}
        {courses.map((c) => (
          <TouchableOpacity
            key={c.id}
            onPress={() => navigation.navigate("Lesson", { courseId: c.id })}
          >
            {/* <List.Item
              style={MyStyles.margin}
              title={c.subject}
              description={moment(c.created_date).fromNow()}
              left={() => (
                <Image style={MyStyles.avatar} source={{ uri: c.image }} />
              )}
            /> */}
            <Item instance={c} />
          </TouchableOpacity>
        ))}
        {loading && page > 1 && <ActivityIndicator />}
      </ScrollView>
    </View>
  );
};
export default Course;

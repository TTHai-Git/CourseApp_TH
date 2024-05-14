import { ActivityIndicator, Text, TouchableOpacity, View } from "react-native";
import MyStyles from "../../configs/styles/MyStyles";
import React from "react";
import APIS, { endpoints } from "../../configs/APIS";
import Item from "../Utils/item";

const Lesson = ({ route, navigation }) => {
  const courseId = route.params?.courseId;
  const [lessons, setLessons] = React.useState(null);

  const loadLessons = async () => {
    try {
      let res = await APIS.get(endpoints["lessons"](courseId));
      setLessons(res.data);
    } catch (ex) {
      console.error(ex);
    }
  };
  React.useEffect(() => {
    loadLessons();
  }, [courseId]);

  return (
    <View style={MyStyles.container}>
      <Text style={MyStyles.subject}>DANH MỤC BÀI HỌC</Text>
      {lessons === null ? (
        <ActivityIndicator />
      ) : (
        <>
          {lessons.map((l) => (
            <TouchableOpacity
              key={l.id}
              onPress={() =>
                navigation.navigate("LessonDetails", { lessonId: l.id })
              }
            >
              <Item instance={l} />
            </TouchableOpacity>
          ))}
        </>
      )}
    </View>
  );
};
export default Lesson;

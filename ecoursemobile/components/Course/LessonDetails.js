import React from "react";
import APIS, { endpoints } from "../../configs/APIS";
import {
  ActivityIndicator,
  Image,
  ScrollView,
  Text,
  View,
  useWindowDimensions,
} from "react-native";
import MyStyles from "../../configs/styles/MyStyles";
import { Card, List } from "react-native-paper";
import RenderHTML from "react-native-render-html";
import isCloseToBottom from "../Utils/utils";
import moment from "moment";

const LessonDetails = ({ route }) => {
  const lessonId = route.params?.lessonId;
  const [lessonDetails, setLessonDetails] = React.useState(null);
  const [comments, setComments] = React.useState(null);
  const { width } = useWindowDimensions();

  const loadLessonDetails = async () => {
    try {
      let res = await APIS.get(endpoints["lesson-details"](lessonId));
      setLessonDetails(res.data);
    } catch (ex) {
      console.error(ex);
    }
  };

  const loadComments = async () => {
    try {
      let res = await APIS.get(endpoints["comments"](lessonId));
      setComments(res.data);
    } catch (ex) {
      console.error(ex);
    }
  };

  React.useEffect(() => {
    loadLessonDetails();
  }, [lessonId]);

  const loadMoreInfo = ({ nativeEvent }) => {
    if (!comments && isCloseToBottom(nativeEvent)) {
      loadComments();
    }
  };

  return (
    <View style={MyStyles.container}>
      <ScrollView onScroll={loadMoreInfo}>
        {lessonDetails === null ? (
          <ActivityIndicator />
        ) : (
          <>
            <Card>
              <Card.Title
                titleStyle={MyStyles.subject}
                title={lessonDetails.subject}
              />
              <Card.Cover source={{ uri: lessonDetails.image }} />
              <Card.Content>
                <RenderHTML
                  contentWidth={width}
                  source={{ html: lessonDetails.content }}
                />
              </Card.Content>
            </Card>
          </>
        )}
        {comments === null ? (
          <ActivityIndicator />
        ) : (
          <>
            {comments.map((c) => (
              <List.Item
                key={c.id}
                style={MyStyles.margin}
                title={c.content}
                description={moment(c.created_date).fromNow()}
                left={() => (
                  <Image
                    style={MyStyles.avatar}
                    source={{ uri: c.user.avatar }}
                  />
                )}
              />
            ))}
          </>
        )}
      </ScrollView>
    </View>
  );
};
export default LessonDetails;

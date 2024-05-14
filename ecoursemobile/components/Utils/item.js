import { List } from "react-native-paper";
import MyStyles from "../../configs/styles/MyStyles";
import { Image } from "react-native";
import moment from "moment";

const Item = ({ instance }) => {
  return (
    <List.Item
      style={MyStyles.margin}
      title={instance.subject}
      description={
        instance.created_date ? moment(instance.created_date).fromNow() : ""
      }
      left={() => (
        <Image style={MyStyles.avatar} source={{ uri: instance.image }} />
      )}
    />
  );
};
export default Item;

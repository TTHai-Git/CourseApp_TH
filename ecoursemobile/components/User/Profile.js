import { useContext } from "react";
import { View, Text } from "react-native";
import { Button } from "react-native-paper";
import { MyUserContext } from "../../configs/Context";
import MyStyles from "../../configs/styles/MyStyles";

const Profile = () => {
  const user = useContext(MyUserContext);
  const dispatch = useContext(MyDispatchContext);

  return (
    <View style={[MyStyles.container, MyStyles.margin]}>
      <Text style={MyStyles.subject}>CHÀO {user.username}!</Text>
      <Button icon="logout" onPress={() => dispatch({ type: "logout" })}>
        Đăng xuất
      </Button>
    </View>
  );
};

export default Profile;

import AsyncStorage from "@react-native-async-storage/async-storage";
import { Text, View } from "react-native";
import MyStyles from "../../configs/styles/MyStyles";
import { useContext, useState } from "react";
import APIS, { authApi, endpoints } from "../../configs/APIS";
import { Button, TextInput } from "react-native-paper";
import { useNavigation } from "@react-navigation/native";
import { MyDispatchContext } from "../../configs/Context";

const Login = ({ navigation }) => {
  const [user, setUser] = useState({});

  const fields = [
    {
      label: "Tên đăng nhập",
      icon: "acount",
      name: "username",
    },
    {
      label: "Mật khẩu",
      icon: "eye",
      name: "password",
      secureTextEntry: true,
    },
  ];

  const [loading, setLoading] = useState(false);
  const nav = useNavigation();
  const dispatch = useContext(MyDispatchContext);

  const updateSate = (field, value) => {
    setUser((current) => {
      return { ...current, [field]: value };
    });
  };

  const login = async () => {
    setLoading(true);

    try {
      let res = await APIS.post(endpoints["login"], {
        ...user,
        client_id: "Vbe8euZZQJoWJ2UzW9wDThg4hJEZHHbhFmnfj7UR",
        client_secret:
          "cVm4w4hSdy4MtwbP4KuNgXkGPeQJ9yrQdBvXHGR6b3e97F2bYqQ81XJ49FEufzjcw4SKwpuOZQiCLsNelHY1MkuYTGBRcSqtWmSlebSUk27WfyDskCB2VeCQihnEKdZ2",
        grant_type: "password",
      });
      console.info(res.data);

      await AsyncStorage.setItem("token", res.data.access_token);

      setTimeout(async () => {
        let user = await authApi(res.data.access_token).get(
          endpoints["current-user"]
        );
        dispatch({
          type: "login",
          payload: user.data,
        });
        nav.navigate("Home");
      }, 100);
    } catch (ex) {
      console.error(ex);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={[MyStyles.container, MyStyles.margin]}>
      <Text style={MyStyles.subject}>ĐĂNG NHẬP NGƯỜI DÙNG</Text>
      {fields.map((c) => (
        <TextInput
          secureTextEntry={c.secureTextEntry}
          value={user[c.name]}
          onChangeText={(t) => updateSate(c.name, t)}
          style={MyStyles.margin}
          key={c.name}
          label={c.label}
          right={<TextInput.Icon icon={c.icon} />}
        />
      ))}
      <Button icon="account" loading={loading} mode="contained" onPress={login}>
        ĐĂNG NHẬP
      </Button>
    </View>
  );
};
export default Login;

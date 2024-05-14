import { NavigationContainer } from "@react-navigation/native";
import Course from "./components/Course/Course";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Lesson from "./components/Course/Lesson";
import LessonDetails from "./components/Course/LessonDetails";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import Register from "./components/User/Register";
import Login from "./components/User/Login";
import { Icon } from "react-native-paper";

const Stack = createNativeStackNavigator();

const MyStack = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen
        name="Course"
        component={Course}
        options={{ title: "Khóa học" }}
      />
      <Stack.Screen
        name="Lesson"
        component={Lesson}
        options={{ title: "bài học" }}
      />
      <Stack.Screen
        name="LessonDetails"
        component={LessonDetails}
        options={{ title: "chi tiết khóa học" }}
      />
    </Stack.Navigator>
  );
};

const Tab = createBottomTabNavigator();
const MyTab = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen
        name="Home"
        component={MyStack}
        options={{
          tabBarIcon: () => <Icon size={30} color="blue" source="home" />,
        }}
      />
      <Tab.Screen
        name="Register"
        component={Register}
        options={{
          tabBarIcon: () => <Icon size={30} color="blue" source="account" />,
        }}
      />
      <Tab.Screen
        name="Login"
        component={Login}
        options={{
          tabBarIcon: () => <Icon size={30} color="blue" source="login" />,
        }}
      />
    </Tab.Navigator>
  );
};

const App = () => {
  return (
    <NavigationContainer>
      <MyTab />
    </NavigationContainer>
  );
};

export default App;

import { NavigationContainer } from "@react-navigation/native";
import Course from "./components/Course/Course";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Lesson from "./components/Course/Lesson";
import LessonDetails from "./components/Course/LessonDetails";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import Register from "./components/User/Register";
import Login from "./components/User/Login";
import { Icon } from "react-native-paper";
import { useContext, useReducer } from "react";
import { MyDispatchContext, MyUserContext } from "./configs/Context";
import MyUserReducer from "./configs/Reducers";
import Profile from "./components/User/Profile";

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
  const user = useContext(MyUserContext);
  return (
    <Tab.Navigator>
      <Tab.Screen
        name="Home"
        component={MyStack}
        options={{
          title: "Khóa học",
          tabBarIcon: () => <Icon size={30} color="blue" source="home" />,
        }}
      />
      {user === null ? (
        <>
          <Tab.Screen
            name="Register"
            component={Register}
            options={{
              title: "Đăng ký",
              tabBarIcon: () => (
                <Icon size={30} color="blue" source="account" />
              ),
            }}
          />
          <Tab.Screen
            name="Login"
            component={Login}
            options={{
              title: "Đăng nhập",
              tabBarIcon: () => <Icon size={30} color="blue" source="login" />,
            }}
          />
        </>
      ) : (
        <>
          <Tab.Screen
            name="Profile"
            component={Profile}
            options={{
              title: user.username,
              tabBarIcon: () => (
                <Icon size={30} color="blue" source="account" />
              ),
            }}
          />
        </>
      )}
    </Tab.Navigator>
  );
};

const App = () => {
  const [user, dispatch] = useReducer(MyUserReducer, null);
  return (
    <NavigationContainer>
      <MyUserContext.Provider value={user}>
        <MyDispatchContext.Provider value={dispatch}>
          <MyTab />
        </MyDispatchContext.Provider>
      </MyUserContext.Provider>
    </NavigationContainer>
  );
};

export default App;

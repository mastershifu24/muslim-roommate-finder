import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { TouchableOpacity, Text } from 'react-native';

import { useAuth } from '../context/AuthContext';

// Auth Screens
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';

// Main Screens
import HomeScreen from '../screens/HomeScreen';
import BrowseProfilesScreen from '../screens/BrowseProfilesScreen';
import ProfileDetailScreen from '../screens/ProfileDetailScreen';
import MyProfileScreen from '../screens/MyProfileScreen';
import MessagesScreen from '../screens/MessagesScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

// Main tab navigator (after login)
function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#28a745',
        tabBarInactiveTintColor: '#999',
        tabBarStyle: {
          paddingBottom: 5,
          paddingTop: 5,
          height: 60,
        },
        tabBarLabelStyle: {
          fontSize: 12,
        },
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          tabBarLabel: 'Home',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>🏠</Text>,
          headerShown: false,
        }}
      />
      <Tab.Screen
        name="Browse"
        component={BrowseProfilesScreen}
        options={{
          tabBarLabel: 'Browse',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>🔍</Text>,
          title: 'Browse Profiles',
        }}
      />
      <Tab.Screen
        name="Messages"
        component={MessagesScreen}
        options={{
          tabBarLabel: 'Messages',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>💬</Text>,
          title: 'Messages',
        }}
      />
      <Tab.Screen
        name="MyProfile"
        component={MyProfileScreen}
        options={{
          tabBarLabel: 'Profile',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>👤</Text>,
          title: 'My Profile',
        }}
      />
    </Tab.Navigator>
  );
}

// Auth navigator (before login)
function AuthStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
      }}
    >
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
    </Stack.Navigator>
  );
}

// Main app navigator
function AppStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen
        name="MainTabs"
        component={MainTabs}
        options={{ headerShown: false }}
      />
      <Stack.Screen
        name="ProfileDetail"
        component={ProfileDetailScreen}
        options={{ title: 'Profile' }}
      />
    </Stack.Navigator>
  );
}

// Root navigator that switches between Auth and App
export default function AppNavigator() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return null; // You could show a loading screen here
  }

  return (
    <NavigationContainer>
      {isAuthenticated ? <AppStack /> : <AuthStack />}
    </NavigationContainer>
  );
}


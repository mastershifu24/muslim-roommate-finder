import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { TouchableOpacity, Text } from 'react-native';

import { useAuth } from '../context/AuthContext';

// Helper to ensure all boolean props in screen options are actual booleans
const normalizeScreenOptions = (options) => {
  if (!options || typeof options !== 'object') return options;
  
  const normalized = { ...options };
  const booleanProps = ['headerShown', 'gestureEnabled', 'animationEnabled', 'fullScreenGestureEnabled'];
  
  booleanProps.forEach(prop => {
    if (prop in normalized) {
      const value = normalized[prop];
      if (typeof value === 'string') {
        console.warn(`⚠️ Found string value for ${prop}:`, value);
        normalized[prop] = value.toLowerCase() === 'true';
      } else {
        normalized[prop] = Boolean(value);
      }
    }
  });
  
  return normalized;
};

// Auth Screens
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';
import TestScreen from '../screens/TestScreen';

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
        options={normalizeScreenOptions({
          tabBarLabel: 'Home',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>🏠</Text>,
          headerShown: false,
        })}
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
  // TEST: Use minimal test screen to isolate issue
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="Test" 
        component={TestScreen}
      />
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
        options={normalizeScreenOptions({ headerShown: false })}
      />
      <Stack.Screen
        name="ProfileDetail"
        component={ProfileDetailScreen}
        options={normalizeScreenOptions({ title: 'Profile' })}
      />
    </Stack.Navigator>
  );
}

// Root navigator that switches between Auth and App
export default function AppNavigator() {
  // TEMPORARY: Bypass auth to test if AuthContext is the issue
  // const authContext = useAuth();
  // const loading = Boolean(authContext?.loading ?? true);
  // const isAuthenticated = Boolean(authContext?.isAuthenticated ?? false);

  // Force show AuthStack for testing
  const loading = false;
  const isAuthenticated = false;

  // Show nothing while loading
  if (loading) {
    return null;
  }

  return (
    <NavigationContainer>
      {isAuthenticated ? <AppStack /> : <AuthStack />}
    </NavigationContainer>
  );
}


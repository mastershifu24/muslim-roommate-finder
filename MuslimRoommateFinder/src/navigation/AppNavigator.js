import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import TestScreen from '../screens/TestScreen';

const Stack = createNativeStackNavigator();

// ABSOLUTE MINIMUM TEST - Try with explicit options object
export default function AppNavigator() {
  const screenOptions = {
    headerShown: false,
  };

  // Ensure all values are proper types
  console.log('🔍 Screen options:', screenOptions);
  console.log('🔍 Screen options types:', {
    headerShown: typeof screenOptions.headerShown,
  });

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={screenOptions}>
        <Stack.Screen 
          name="Test" 
          component={TestScreen}
          options={{}}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}


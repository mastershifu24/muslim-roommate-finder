import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import TestScreen from '../screens/TestScreen';

// Debug: Check if createNativeStackNavigator works
console.log('🔍 createNativeStackNavigator:', typeof createNativeStackNavigator);

const Stack = createNativeStackNavigator();

// Debug: Check if Stack was created
console.log('🔍 Stack:', Stack);
console.log('🔍 Stack.Navigator:', Stack?.Navigator);
console.log('🔍 Stack.Screen:', Stack?.Screen);

// ABSOLUTE MINIMUM TEST - Try with explicit options object
export default function AppNavigator() {
  // Check if Stack exists
  if (!Stack || !Stack.Navigator || !Stack.Screen) {
    console.error('❌ Stack navigator not created properly!', Stack);
    return (
      <NavigationContainer>
        <TestScreen />
      </NavigationContainer>
    );
  }

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


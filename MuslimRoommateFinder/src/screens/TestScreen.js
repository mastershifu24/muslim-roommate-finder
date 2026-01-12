import React from 'react';
import { View, Text } from 'react-native';

export default function TestScreen({ navigation, route }) {
  // Explicitly accept navigation and route props even if we don't use them
  // This ensures React Navigation can pass them correctly
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Test Screen - Minimal</Text>
    </View>
  );
}


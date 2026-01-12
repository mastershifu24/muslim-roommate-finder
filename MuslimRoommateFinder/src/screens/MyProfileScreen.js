import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  Switch,
} from 'react-native';
import { useAuth } from '../context/AuthContext';
import { profileAPI } from '../api/client';

export default function MyProfileScreen({ navigation }) {
  const { profile, refreshProfile, logout } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    gender: '',
    city: '',
    state: '',
    zip_code: '',
    bio: '',
    contact_email: '',
    whatsapp_number: '',
    only_eats_zabihah: false,
    prayer_friendly: false,
    guests_allowed: false,
    is_looking_for_room: false,
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (profile) {
      setFormData({
        name: profile.name || '',
        age: profile.age?.toString() || '',
        gender: profile.gender || '',
        city: profile.city || '',
        state: profile.state || '',
        zip_code: profile.zip_code || '',
        bio: profile.bio || '',
        contact_email: profile.contact_email || '',
        whatsapp_number: profile.whatsapp_number || '',
        only_eats_zabihah: Boolean(profile.only_eats_zabihah),
        prayer_friendly: Boolean(profile.prayer_friendly),
        guests_allowed: Boolean(profile.guests_allowed),
        is_looking_for_room: Boolean(profile.is_looking_for_room),
      });
    }
  }, [profile]);

  const updateField = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  const handleSave = async () => {
    try {
      setLoading(true);
      
      // Prepare data
      const dataToSend = {
        ...formData,
        age: formData.age ? parseInt(formData.age) : null,
      };
      
      await profileAPI.updateProfile(dataToSend);
      await refreshProfile();
      
      Alert.alert('Success', 'Profile updated successfully!');
    } catch (error) {
      console.error('Failed to update profile:', error);
      Alert.alert('Error', 'Failed to update profile. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Logout', onPress: logout, style: 'destructive' },
      ]
    );
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Basic Information</Text>
        
        <Text style={styles.label}>Name *</Text>
        <TextInput
          style={styles.input}
          value={formData.name}
          onChangeText={(value) => updateField('name', value)}
          placeholder="Your full name"
        />

        <Text style={styles.label}>Age</Text>
        <TextInput
          style={styles.input}
          value={formData.age}
          onChangeText={(value) => updateField('age', value)}
          placeholder="Your age"
          keyboardType="numeric"
        />

        <Text style={styles.label}>Gender</Text>
        <View style={styles.genderButtons}>
          <TouchableOpacity
            style={[
              styles.genderButton,
              formData.gender === 'M' && styles.genderButtonActive,
            ]}
            onPress={() => updateField('gender', 'M')}
          >
            <Text
              style={[
                styles.genderButtonText,
                formData.gender === 'M' && styles.genderButtonTextActive,
              ]}
            >
              Male
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[
              styles.genderButton,
              formData.gender === 'F' && styles.genderButtonActive,
            ]}
            onPress={() => updateField('gender', 'F')}
          >
            <Text
              style={[
                styles.genderButtonText,
                formData.gender === 'F' && styles.genderButtonTextActive,
              ]}
            >
              Female
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Location</Text>
        
        <Text style={styles.label}>City *</Text>
        <TextInput
          style={styles.input}
          value={formData.city}
          onChangeText={(value) => updateField('city', value)}
          placeholder="e.g., Charleston"
        />

        <Text style={styles.label}>State *</Text>
        <TextInput
          style={styles.input}
          value={formData.state}
          onChangeText={(value) => updateField('state', value)}
          placeholder="e.g., SC"
        />

        <Text style={styles.label}>ZIP Code</Text>
        <TextInput
          style={styles.input}
          value={formData.zip_code}
          onChangeText={(value) => updateField('zip_code', value)}
          placeholder="e.g., 29401"
          keyboardType="numeric"
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>About Me</Text>
        
        <TextInput
          style={[styles.input, styles.textArea]}
          value={formData.bio}
          onChangeText={(value) => updateField('bio', value)}
          placeholder="Tell others about yourself..."
          multiline
          numberOfLines={4}
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Contact Information</Text>
        
        <Text style={styles.label}>Email</Text>
        <TextInput
          style={styles.input}
          value={formData.contact_email}
          onChangeText={(value) => updateField('contact_email', value)}
          placeholder="your.email@example.com"
          keyboardType="email-address"
          autoCapitalize="none"
        />

        <Text style={styles.label}>WhatsApp Number</Text>
        <Text style={styles.helpText}>Include country code (e.g., +12025551234)</Text>
        <TextInput
          style={styles.input}
          value={formData.whatsapp_number}
          onChangeText={(value) => updateField('whatsapp_number', value)}
          placeholder="+1234567890"
          keyboardType="phone-pad"
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Preferences</Text>
        
        <View style={styles.switchRow}>
          <Text style={styles.switchLabel}>🍖 Only eat Zabihah</Text>
          <Switch
            value={Boolean(formData.only_eats_zabihah)}
            onValueChange={(value) => updateField('only_eats_zabihah', value)}
            trackColor={{ false: '#767577', true: '#28a745' }}
          />
        </View>

        <View style={styles.switchRow}>
          <Text style={styles.switchLabel}>🕌 Prayer friendly</Text>
          <Switch
            value={Boolean(formData.prayer_friendly)}
            onValueChange={(value) => updateField('prayer_friendly', value)}
            trackColor={{ false: '#767577', true: '#28a745' }}
          />
        </View>

        <View style={styles.switchRow}>
          <Text style={styles.switchLabel}>👥 Guests allowed</Text>
          <Switch
            value={Boolean(formData.guests_allowed)}
            onValueChange={(value) => updateField('guests_allowed', value)}
            trackColor={{ false: '#767577', true: '#28a745' }}
          />
        </View>

        <View style={styles.switchRow}>
          <Text style={styles.switchLabel}>🔍 Looking for room</Text>
          <Switch
            value={Boolean(formData.is_looking_for_room)}
            onValueChange={(value) => updateField('is_looking_for_room', value)}
            trackColor={{ false: '#767577', true: '#28a745' }}
          />
        </View>
      </View>

      <TouchableOpacity
        style={[styles.saveButton, loading && styles.buttonDisabled]}
        onPress={handleSave}
        disabled={loading}
      >
        <Text style={styles.saveButtonText}>
          {loading ? 'Saving...' : 'Save Profile'}
        </Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
        <Text style={styles.logoutButtonText}>Logout</Text>
      </TouchableOpacity>

      <View style={styles.bottomPadding} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  section: {
    backgroundColor: '#fff',
    padding: 20,
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 5,
    marginTop: 10,
  },
  helpText: {
    fontSize: 12,
    color: '#999',
    marginBottom: 5,
  },
  input: {
    backgroundColor: '#f5f5f5',
    padding: 12,
    borderRadius: 8,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  textArea: {
    height: 100,
    textAlignVertical: 'top',
  },
  genderButtons: {
    flexDirection: 'row',
    gap: 10,
  },
  genderButton: {
    flex: 1,
    padding: 12,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: '#ddd',
    alignItems: 'center',
  },
  genderButtonActive: {
    borderColor: '#28a745',
    backgroundColor: '#28a745',
  },
  genderButtonText: {
    fontSize: 16,
    color: '#666',
  },
  genderButtonTextActive: {
    color: '#fff',
    fontWeight: 'bold',
  },
  switchRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  switchLabel: {
    fontSize: 16,
    color: '#333',
  },
  saveButton: {
    backgroundColor: '#28a745',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    margin: 20,
    marginBottom: 10,
  },
  buttonDisabled: {
    backgroundColor: '#95d5a5',
  },
  saveButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  logoutButton: {
    backgroundColor: '#dc3545',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginHorizontal: 20,
  },
  logoutButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  bottomPadding: {
    height: 40,
  },
});


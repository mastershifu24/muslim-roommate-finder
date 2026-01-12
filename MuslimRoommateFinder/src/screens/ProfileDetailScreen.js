import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  Image,
  TouchableOpacity,
  Linking,
  ActivityIndicator,
} from 'react-native';
import { profileAPI } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function ProfileDetailScreen({ route, navigation }) {
  const { profileId } = route.params;
  const { profile: myProfile } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [compatibility, setCompatibility] = useState(null);

  useEffect(() => {
    loadProfile();
  }, [profileId]);

  // Helper to normalize boolean values (API might return strings)
  const normalizeBooleans = (profile) => ({
    ...profile,
    only_eats_zabihah: Boolean(profile.only_eats_zabihah),
    prayer_friendly: Boolean(profile.prayer_friendly),
    guests_allowed: Boolean(profile.guests_allowed),
    is_looking_for_room: Boolean(profile.is_looking_for_room),
  });

  const loadProfile = async () => {
    try {
      setLoading(true);
      const data = await profileAPI.getProfileById(profileId);
      const normalizedProfile = normalizeBooleans(data);
      setProfile(normalizedProfile);
      
      // Calculate compatibility if we have our profile
      if (myProfile) {
        const score = calculateCompatibility(normalizedProfile);
        setCompatibility(score);
      }
    } catch (error) {
      console.error('Failed to load profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateCompatibility = (otherProfile) => {
    if (!myProfile) return null;
    
    // Ensure both profiles have normalized booleans for comparison
    const normalizedMyProfile = {
      only_eats_zabihah: Boolean(myProfile.only_eats_zabihah),
      prayer_friendly: Boolean(myProfile.prayer_friendly),
      guests_allowed: Boolean(myProfile.guests_allowed),
    };
    const normalizedOther = {
      only_eats_zabihah: Boolean(otherProfile.only_eats_zabihah),
      prayer_friendly: Boolean(otherProfile.prayer_friendly),
      guests_allowed: Boolean(otherProfile.guests_allowed),
    };
    
    let score = 0;
    if (normalizedMyProfile.only_eats_zabihah === normalizedOther.only_eats_zabihah) score += 20;
    if (normalizedMyProfile.prayer_friendly === normalizedOther.prayer_friendly) score += 20;
    
    if (myProfile.city && otherProfile.city) {
      if (myProfile.city.toLowerCase() === otherProfile.city.toLowerCase()) {
        score += 30;
      } else if (myProfile.state && otherProfile.state) {
        if (myProfile.state.toLowerCase() === otherProfile.state.toLowerCase()) {
          score += 15;
        }
      }
    }
    
    if (myProfile.age && otherProfile.age) {
      const ageDiff = Math.abs(myProfile.age - otherProfile.age);
      if (ageDiff <= 3) score += 20;
      else if (ageDiff <= 5) score += 15;
      else if (ageDiff <= 10) score += 10;
      else if (ageDiff <= 15) score += 5;
    }
    
    if (normalizedMyProfile.guests_allowed === normalizedOther.guests_allowed) score += 10;
    
    return Math.min(score, 100);
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#28a745';
    if (score >= 60) return '#ffc107';
    return '#6c757d';
  };

  const openWhatsApp = () => {
    if (profile?.whatsapp_number) {
      const cleanNumber = profile.whatsapp_number.replace(/[^\d+]/g, '');
      Linking.openURL(`https://wa.me/${cleanNumber}`);
    }
  };

  const openEmail = () => {
    if (profile?.contact_email) {
      Linking.openURL(`mailto:${profile.contact_email}`);
    }
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#28a745" />
      </View>
    );
  }

  if (!profile) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>Profile not found</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        {profile.profile_photo && (
          <Image source={{ uri: profile.profile_photo }} style={styles.photo} />
        )}
        <Text style={styles.name}>{profile.name}</Text>
        <Text style={styles.location}>
          {profile.city}, {profile.state} {profile.zip_code}
        </Text>
        {profile.age && (
          <Text style={styles.age}>{profile.age} years old • {profile.gender_display}</Text>
        )}
        
        {compatibility !== null && (
          <View
            style={[
              styles.compatibilityBadge,
              { backgroundColor: getScoreColor(compatibility) },
            ]}
          >
            <Text style={styles.compatibilityText}>
              {compatibility}% Compatible
            </Text>
          </View>
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>About</Text>
        {profile.bio ? (
          <Text style={styles.bioText}>{profile.bio}</Text>
        ) : (
          <Text style={styles.placeholderText}>No bio provided</Text>
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Preferences</Text>
        <View style={styles.badges}>
          {profile.only_eats_zabihah && (
            <View style={styles.badgeContainer}>
              <Text style={styles.badgeEmoji}>🍖</Text>
              <Text style={styles.badgeText}>Only eats Zabihah</Text>
            </View>
          )}
          {profile.prayer_friendly && (
            <View style={styles.badgeContainer}>
              <Text style={styles.badgeEmoji}>🕌</Text>
              <Text style={styles.badgeText}>Prayer friendly</Text>
            </View>
          )}
          {profile.guests_allowed && (
            <View style={styles.badgeContainer}>
              <Text style={styles.badgeEmoji}>👥</Text>
              <Text style={styles.badgeText}>Guests allowed</Text>
            </View>
          )}
          {profile.is_looking_for_room && (
            <View style={styles.badgeContainer}>
              <Text style={styles.badgeEmoji}>🔍</Text>
              <Text style={styles.badgeText}>Looking for room</Text>
            </View>
          )}
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Contact</Text>
        
        {profile.whatsapp_number && (
          <TouchableOpacity style={styles.whatsappButton} onPress={openWhatsApp}>
            <Text style={styles.whatsappText}>💬 Message on WhatsApp</Text>
          </TouchableOpacity>
        )}
        
        {profile.contact_email && (
          <TouchableOpacity style={styles.emailButton} onPress={openEmail}>
            <Text style={styles.emailText}>📧 Send Email</Text>
          </TouchableOpacity>
        )}
        
        {!profile.whatsapp_number && !profile.contact_email && (
          <Text style={styles.placeholderText}>
            No contact information provided
          </Text>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#fff',
    padding: 20,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  photo: {
    width: 120,
    height: 120,
    borderRadius: 60,
    marginBottom: 15,
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  location: {
    fontSize: 16,
    color: '#666',
    marginBottom: 5,
  },
  age: {
    fontSize: 14,
    color: '#999',
    marginBottom: 15,
  },
  compatibilityBadge: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 25,
    marginTop: 10,
  },
  compatibilityText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  section: {
    backgroundColor: '#fff',
    padding: 20,
    marginTop: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  bioText: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  },
  placeholderText: {
    fontSize: 14,
    color: '#999',
    fontStyle: 'italic',
  },
  badges: {
    flexDirection: 'column',
  },
  badgeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  badgeEmoji: {
    fontSize: 24,
    marginRight: 10,
  },
  badgeText: {
    fontSize: 16,
    color: '#333',
  },
  whatsappButton: {
    backgroundColor: '#25D366',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 10,
  },
  whatsappText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  emailButton: {
    backgroundColor: '#007bff',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  emailText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  errorText: {
    fontSize: 18,
    color: '#999',
  },
});


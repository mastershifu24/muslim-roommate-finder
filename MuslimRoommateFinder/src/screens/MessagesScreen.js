import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { messageAPI } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function MessagesScreen({ navigation }) {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadMessages();
  }, []);

  const loadMessages = async () => {
    try {
      setLoading(true);
      const data = await messageAPI.getInbox();
      setMessages(data);
    } catch (error) {
      console.error('Failed to load messages:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return 'Today';
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  const renderMessage = ({ item }) => {
    const isReceived = item.recipient.id === user?.id;
    const otherPerson = isReceived ? item.sender_profile : item.recipient_profile;

    return (
      <TouchableOpacity
        style={[
          styles.messageCard,
          !item.is_read && isReceived && styles.unreadMessage,
        ]}
        onPress={() => {
          if (otherPerson) {
            navigation.navigate('ProfileDetail', { profileId: otherPerson.id });
          }
        }}
      >
        <View style={styles.messageHeader}>
          <Text style={styles.senderName}>
            {isReceived ? 'From' : 'To'}: {otherPerson?.name || 'Unknown'}
          </Text>
          <Text style={styles.messageDate}>{formatDate(item.timestamp)}</Text>
        </View>
        <Text style={styles.messageContent} numberOfLines={2}>
          {item.content}
        </Text>
        {!item.is_read && isReceived && (
          <View style={styles.unreadBadge}>
            <Text style={styles.unreadText}>NEW</Text>
          </View>
        )}
      </TouchableOpacity>
    );
  };

  return (
    <View style={styles.container}>
      {messages.length === 0 && !loading ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyText}>No messages yet</Text>
          <Text style={styles.emptySubtext}>
            Start connecting with roommates to send messages!
          </Text>
        </View>
      ) : (
        <FlatList
          data={messages}
          renderItem={renderMessage}
          keyExtractor={(item) => item.id.toString()}
          refreshControl={
            <RefreshControl refreshing={loading} onRefresh={loadMessages} />
          }
          contentContainerStyle={styles.listContent}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  listContent: {
    padding: 15,
  },
  messageCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 15,
    marginBottom: 10,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  unreadMessage: {
    borderLeftWidth: 4,
    borderLeftColor: '#28a745',
  },
  messageHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  senderName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  messageDate: {
    fontSize: 12,
    color: '#999',
  },
  messageContent: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  unreadBadge: {
    position: 'absolute',
    top: 10,
    right: 10,
    backgroundColor: '#28a745',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  unreadText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: 'bold',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#666',
    marginBottom: 10,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
  },
});


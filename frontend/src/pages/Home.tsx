import React, { useEffect, useState } from 'react';
import { getChannels } from '../services/api';

interface Channel {
  id: number;
  channel_name: string;
  channel_icon_url: string;
}

const ChannelList = () => {
  const [channels, setChannels] = useState<Channel[]>([]);

  useEffect(() => {
    getChannels().then(response => {
      setChannels(response.data as Channel[]);
    }).catch(error => {
      console.error('Error fetching channels:', error);
    });
  }, []);

  return (
    <div>
      <h3>Subscribed Channels List</h3>
      <ul>
        {channels.map(channel => (
          <li key={channel.id}>
            <h6>{channel.channel_name}</h6>
            <img src={channel.channel_icon_url} alt={channel.channel_name} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChannelList;

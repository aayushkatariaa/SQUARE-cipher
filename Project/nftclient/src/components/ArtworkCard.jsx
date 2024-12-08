import React, { useState } from 'react';
import axios from 'axios';

const ArtworkCard = ({ artwork }) => {
  const [decryptedMetadata, setDecryptedMetadata] = useState(null);
  const [secretKey, setSecretKey] = useState('');

  const decryptMetadata = async () => {
    const response = await axios.get(`http://localhost:8000/decrypt_metadata/${artwork._id}?secret_key=${secretKey}`);
    setDecryptedMetadata(response.data.decrypted_metadata);
  };

  return (
    <div>
      <img src={artwork.image_url} alt={artwork.title} width="200" />
      <h2>{artwork.title}</h2>
      <p>{artwork.price}</p>
      {decryptedMetadata ? (
        <div>
          <h3>Decrypted Metadata:</h3>
          <pre>{decryptedMetadata}</pre>
        </div>
      ) : (
        <div>
          <input
            type="text"
            placeholder="Enter secret key"
            value={secretKey}
            onChange={(e) => setSecretKey(e.target.value)}
          />
          <button onClick={decryptMetadata}>Decrypt Metadata</button>
        </div>
      )}
    </div>
  );
};

export default ArtworkCard;

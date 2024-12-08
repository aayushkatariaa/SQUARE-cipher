import React, { useState } from 'react';
import axios from 'axios';

const UploadArtworkForm = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');
  const [image, setImage] = useState(null);
  const [secretKey, setSecretKey] = useState('');

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', image);
    formData.append('title', title);
    formData.append('description', description);
    formData.append('price', price);
    formData.append('secret_key', secretKey);

    await axios.post('http://localhost:8000/upload_artwork/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    setTitle('');
    setDescription('');
    setPrice('');
    setImage(null);
    setSecretKey('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Upload Artwork</h2>
      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <input
        type="text"
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <input
        type="number"
        placeholder="Price"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
      />
      <input type="file" onChange={handleImageChange} />
      <input
        type="text"
        placeholder="Secret Key"
        value={secretKey}
        onChange={(e) => setSecretKey(e.target.value)}
      />
      <button type="submit">Upload</button>
    </form>
  );
};

export default UploadArtworkForm;

import React, { useState, useEffect, useContext } from "react";
import Cookies from "js-cookie";
import {
  Tab,
  Tabs,
  Modal,
  Box,
  TextField,
  Button,
  Card,
  CardMedia,
  CardContent,
  Typography,
  CardActions,
} from "@mui/material";
import axios from "axios";
import { AuthApi, TokenApi } from "../App";

const Home = () => {
  const Auth = useContext(AuthApi);
  const Token = useContext(TokenApi);
  const [data, setData] = useState([]);
  const [wallet,setWallet]= useState(0);
  const [ownedNfts, setOwnedNfts] = useState([]);
  const [tabValue, setTabValue] = useState(0);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    image_url: "",
    title: "",
    description: "",
    price: "",
  });

  const token = Token.token;
  const headers = {
    Authorization: `Bearer ${token}`,
  };

  const handleLogout = () => {
    Auth.setAuth(false);
    localStorage.removeItem("access_token");
    window.location.reload(); // Redirect to login or refresh
  };

  const fetchMarketplaceNfts = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/artworks", { headers });
      setData(response.data);
    } catch (error) {
      console.error("Failed to fetch marketplace NFTs", error);
    }
  };

  const fetchOwnedNfts = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/owned", { headers });
      setOwnedNfts(response.data.nfts);
    } catch (error) {
      console.error("Failed to fetch owned NFTs", error);
    }
  };

  const handleVerify = (ownerId) => {
    alert(`Owner ID: ${ownerId}`);
  };

  const handleBuy = async (artworkId) => {
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/buy_nft/${artworkId}`,
        {},
        { headers }
      );
      alert("Artwork purchased successfully!");
      fetchMarketplaceNfts(); // Refresh the marketplace after buying
      fetchOwnedNfts(); // Refresh owned NFTs
    } catch (error) {
      console.error("Failed to buy artwork", error);
      alert("Failed to purchase artwork.");
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/upload_artwork", formData, {
        headers,
      });
      alert("Artwork created successfully");
      setIsModalOpen(false);
      setFormData({ image_url: "", title: "", description: "", price: "" });
      fetchMarketplaceNfts();
    } catch (error) {
      console.error("Failed to create artwork", error);
    }
  };
  const fetchWalletBalance = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/wallet_balance", { headers });
      const balance = response.data.wallet_balance;
      setWallet(balance);
    } catch (error) {
      console.error("Failed to fetch wallet balance", error);
    }
  };

  useEffect(() => {
    fetchMarketplaceNfts();
    fetchOwnedNfts();
    fetchWalletBalance();
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Welcome to NFT Marketplace</h2>
      <Button
        variant="contained"
        color="primary"
        onClick={() => setIsModalOpen(true)}
        style={{ marginBottom: "20px" }}
      >
        Make Artwork
      </Button>
      <Button variant="outlined" color="secondary" onClick={handleLogout} style={{ marginLeft: "10px" }}>
        Logout
      </Button>
      <Typography variant="h6" style={{ marginTop: "20px" }}>
        Wallet Balance: ${wallet}
      </Typography>

      <Tabs value={tabValue} onChange={handleTabChange} centered>
        <Tab label="NFT Marketplace" />
        <Tab label="Owned NFTs" />
      </Tabs>

      {tabValue === 0 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: "20px", marginTop: "20px" }}>
          {data.map((nft) => (
            <Card key={nft.id} style={{ width: "300px" }}>
              <CardMedia component="img" height="200" image={nft.image_url} alt={nft.title} />
              <CardContent>
                <Typography variant="h6">{nft.title}</Typography>
                <Typography variant="body2">{nft.description}</Typography>
                <Typography variant="body2">{nft.encrypted_metadata}</Typography>
                <Typography variant="subtitle1" color="primary">
                  ${nft.price}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  color="primary"
                  onClick={() => handleVerify(nft.owner._id)}
                >
                  Verify
                </Button>
                <Button
                  size="small"
                  color="secondary"
                  onClick={() => handleBuy(nft.id)}
                >
                  Buy
                </Button>
              </CardActions>
            </Card>
          ))}
        </div>
      )}

      {tabValue === 1 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: "20px", marginTop: "20px" }}>
          {ownedNfts.map((nft) => (
            <Card key={nft.id} style={{ width: "300px" }}>
              <CardMedia component="img" height="200" image={nft.image} alt={nft.name} />
              <CardContent>
                <Typography variant="h6">{nft.name}</Typography>
                <Typography variant="body2">{nft.description}</Typography>
                <Typography variant="subtitle1" color="primary">
                  ${nft.price}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <Modal open={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <Box
          style={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 400,
            backgroundColor: "white",
            padding: "20px",
            borderRadius: "8px",
            boxShadow: "0 0 10px rgba(0, 0, 0, 0.25)",
          }}
        >
          <h3>Create Artwork</h3>
          <form onSubmit={handleFormSubmit}>
            <TextField
              label="Image URL"
              name="image_url"
              value={formData.image_url}
              onChange={handleInputChange}
              fullWidth
              margin="normal"
              required
            />
            <TextField
              label="Title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              fullWidth
              margin="normal"
              required
            />
            <TextField
              label="Description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              fullWidth
              margin="normal"
              required
            />
            <TextField
              label="Price"
              name="price"
              type="number"
              value={formData.price}
              onChange={handleInputChange}
              fullWidth
              margin="normal"
              required
            />
            <Button type="submit" variant="contained" color="primary" fullWidth style={{ marginTop: "10px" }}>
              Submit
            </Button>
          </form>
        </Box>
      </Modal>
    </div>
  );
};

export default Home;

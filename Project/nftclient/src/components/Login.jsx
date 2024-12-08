import React, { useState } from 'react';
import { ChevronRight } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Eye, EyeOff } from 'lucide-react';
import axios from 'axios';
const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errorMessage, setErrorMessage] = useState('');
  const [passwordVisible, setPasswordVisible] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    try {
      const response = await axios.post("http://127.0.0.1:8000/login", formData);
      const token = response.data.access_token;
      localStorage.setItem('access_token', token);
      toast.success('Login successful!');
      navigate('/'); // Redirect to dashboard or desired route
    } catch (error) {
      const message = error.response?.data?.message || 'Login failed';
      setErrorMessage(message);
      toast.error(message);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-50">
      <ToastContainer />
      <div className="flex w-full max-w-4xl h-[480px] rounded-lg overflow-hidden shadow-lg">
        {/* Left Panel - Login Form */}
        <div className="w-1/2 bg-white p-8 flex flex-col justify-center">
          <h2 className="text-2xl font-semibold mb-6">Log In to Your Account</h2>

          {errorMessage && <p className="text-red-500 mb-4">{errorMessage}</p>}

          <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              className="p-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-[#E7DBCD]"
              required
            />
            <div className="relative">
              <input
                type={passwordVisible ? 'text' : 'password'}
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                className="p-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-[#E7DBCD] w-full"
                required
              />
              <button
                type="button"
                className="absolute right-3 top-3 text-gray-500"
                onClick={() => setPasswordVisible(!passwordVisible)}
              >
                {passwordVisible ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
            <button type="submit" className="bg-[#B39984] text-white p-3 rounded-lg font-medium hover:bg-[#E7DBCD] transition-colors">
              Log In
            </button>
          </form>
        </div>

        {/* Right Panel - Welcome Message */}
        <div className="w-1/2 bg-[#B39984] p-8 flex flex-col justify-center items-start text-white relative">
          <img src="/WhiteLogo.png" alt="Arissto Icon" className="mb-6" />
          <h3 className="text-3xl font-semibold mb-4">New Here?</h3>
          <p className="mb-8 text-teal-50">Create an account to get started!</p>
          <Link to="/register" className="px-6 py-2 rounded-lg border-2 border-white text-white font-medium hover:bg-white hover:text-[#E7DBCD] transition-colors flex items-center gap-2">
            Sign Up
            <ChevronRight size={20} />
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;

import React, { useState } from 'react';
import { ChevronRight } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Eye, EyeOff } from 'lucide-react';
import axios from 'axios';

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [passwordVisible, setPasswordVisible] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const validatePassword = (password) => {
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(password);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');

    if (!validatePassword(formData.password)) {
      setErrorMessage('Password must have at least 8 characters, an uppercase letter, a number, and a special character.');
      toast.error('Password does not meet the requirements');
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/register", formData);
      setSuccessMessage('Account created successfully! Please log in.');
      toast.success('Account created successfully!');
      setFormData({ username: '', email: '', password: '' });
      setTimeout(() => navigate('/login'), 2000); // Redirect to login after 2 seconds
    } catch (error) {
      const message = error.response?.data?.message || 'Failed to create account';
      setErrorMessage(message);
      toast.error(message);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-50">
      <ToastContainer />
      <div className="flex w-full max-w-4xl h-[480px] rounded-lg overflow-hidden shadow-lg">
        {/* Left Panel - Signup Form */}
        <div className="w-1/2 bg-white p-8 flex flex-col justify-center">
          <h2 className="text-2xl font-semibold mb-6">Create Your Account</h2>

          {errorMessage && <p className="text-red-500 mb-4">{errorMessage}</p>}
          {successMessage && <p className="text-green-500 mb-4">{successMessage}</p>}

          <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              className="p-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-[#E7DBCD]"
              required
            />
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
                type={passwordVisible ? "text" : "password"}
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
              Sign Up
            </button>
          </form>
        </div>

        {/* Right Panel - Welcome Message */}
        <div className="w-1/2 bg-[#B39984] p-8 flex flex-col justify-center items-start text-white relative">
          <img src="/WhiteLogo.png" alt="Arissto Icon" className="mb-6" />
          <h3 className="text-3xl font-semibold mb-4">Already a Member?</h3>
          <p className="mb-8 text-teal-50">Log in to your account to continue your journey!</p>
          <Link to="/login" className="px-6 py-2 rounded-lg border-2 border-white text-white font-medium hover:bg-white hover:text-[#E7DBCD] transition-colors flex items-center gap-2">
            Log In
            <ChevronRight size={20} />
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Register;

# 🦁 PSU Auction Hub

An exclusive auction platform for Penn State students to buy and sell items! Built using Flask, SQLite, JavaScript, HTML, and CSS for seamless functionality and an intuitive user experience.

## 📖 Table of Contents

- About
- Features
- Tech Stack
- Usage

## 📜 About

LionAuction is a platform tailored for Penn State students, enabling a safe and efficient way to auction off items like textbooks, dorm decor, electronics, and more!

- 🔒 Penn State Verified Accounts Only
- 🛒 Dynamic Listings and Bidding System
- 📈 Real-Time Updates for Auctions
Whether you're decluttering your dorm or looking for affordable student deals, PSU Auction Hub has you covered.


# ✨ Features

- User Authentication & Roles: Supports multiple user types (Buyer, Seller, Helpdesk) with customized login flows and session management using cookies.
- Auction Listings Management: Sellers can create, edit, and delete auction listings with detailed information (category, title, description, reserve price, etc.).
- Completed Transaction Tracking: Keeps track of completed transactions, ensuring payment has been made before listing a transaction as completed.
- Search & Filter Functionality: Provides search functionality for auction listings by title or category, allowing users to easily find relevant items.
- Dynamic Bid Placement: Enables users to place bids, ensuring bids are higher than the current bid and prevents consecutive bidding from the same user.
- Transaction History: Allows users (both buyers and sellers) to view completed transactions, including details like buyer, seller, payment, and transaction date.
- Helpdesk Integration: Features a helpdesk system where support staff can view and manage support requests associated with their email.
- Listings by Category: Organizes listings into distinct categories with subcategories, enabling easier navigation.
- Profile Management: Users can view and manage their profile, which includes personal details, contact information, and transaction history.
- Auction Status Management: Automatically handles auction listing statuses, preventing the editing of finished or non-active listings, with user-friendly error pages when needed.
- Database Integration: Uses SQLite for data storage, including tables for users, transactions, listings, requests, and ratings.
- Secure Payment Handling: Integrates a secure payment flow that ensures transactions are completed before listings are finalized.
- Flash Messaging: Implements flash messages to inform users about errors or successful actions (e.g., bid issues, successful updates).

## 🛠 Tech Stack

| Technology | Purpose| 
|-----------------|-----------------|
| Flask | 	Backend framework for API and routing  |
| SQLite | Lightweight database for storing data   | 
| Python  | Backend programming language for logic and processing  |
| Javascript  | Dynamic and interactive user interface  |
| HTML + CSS  | Structure and styling for the frontend  |

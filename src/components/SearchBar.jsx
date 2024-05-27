import React, { useEffect, useState } from "react";
import { FaSearch } from "react-icons/fa";
import axios from "axios";

import "./SearchBar.css";

export const SearchBar = ({ setResults, data, setSuggestions }) => {
    const [input, setInput] = useState("");

    useEffect(()=>{
        setInput(data)
    },[data])

    const fetchData = async (value, shouldappend) => {
        try {
            await axios.post("http://localhost:5000/search", {
                query: value,
                shouldappend: shouldappend
            })
                .then((response) => setResults(response.data))
        } catch (error) {
            console.error("Error fetching search results:", error);
        }
    };

    const handleChange = (value) => {
        setInput(value);
        fetchData(value, false);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        fetchData(input, true);
        setSuggestions([]);
    };

    const handleSearch = () => {
        fetchData(input, true);
        setSuggestions([]);
    };

    return (
        <form className="input-wrapper" onSubmit={handleSubmit}>
            <div className="search-icon-wrapper" onClick={handleSearch}>
                <FaSearch id="search-icon" />
            </div>
            <input
                placeholder="Type to search..."
                value={input}
                onChange={(e) => handleChange(e.target.value)}
            />
        </form>
    );
};
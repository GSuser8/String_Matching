import React, { useState } from "react";
import { SearchResult } from "./SearchResult";
import "./SearchResultsList.css";

export const SearchResultsList = ({ results, setData, setSuggestions }) => {
    const handleClick = (s)=>{
        setData(s);
        setSuggestions([]);
    };

    return (
        <div className="results-list">
            {results.map((result, id) => {
                return <SearchResult key={id} result={result} handleClick={() => handleClick(result)} />;
            })}
        </div>
    );
};
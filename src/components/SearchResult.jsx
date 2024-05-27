import React from "react";

import "./SearchResult.css";

export const SearchResult = ({ result, handleClick }) => {
    return (
        <div className="search-result"
            onClick={()=>handleClick(result)}
        >
            {result}
        </div>
    );
};

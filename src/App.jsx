import { useState } from "react";
import "./App.css";
import { SearchBar } from "./components/SearchBar";
import { SearchResultsList } from "./components/SearchResultsList";

function App() {
    const [results, setResults] = useState([]);
    const [data, setData] =useState("")
    return (
      <div className="App">
        <div id="blob1"></div>
        <div id="blob2"></div>
        <div id="blob3"></div>
        <div id="blob4"></div>

        <div class="navbar">
          <div class="to_side"> 
            <div id="Mail">Mail</div>
            <div id="Settings">Settings</div>
            <div id="Account">Account</div>
          </div>
        </div>

        <div class="heading">StringMatch</div>
        <div className="App">
            <div className="search-bar-container">
                <SearchBar setResults={setResults} data={data}/>
                {/* {results && results.length > 0 && <SearchResultsList results={results} />} */}
                <SearchResultsList results={results} setData={setData}/>
            </div>
        </div>
        <div id="Footer_el">
          <footer>
            <div id="india">India</div>
            <div id="Footerdiv">
              <div class="contents">
                <div class="text">About</div>
                <div class="text">Advertising</div>
                <div class="text">Business</div>
                <div class="text">How search works</div>
              </div>
              <div class="contents">
                <div class="text">Privacy</div>
                <div class="text">Terms</div>
                <div class="text">Settings</div>
              </div>
            </div>
          </footer>
      </div>
    </div>
    );
}

export default App;
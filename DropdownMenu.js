import React from 'react';
import { Form } from 'react-bootstrap';
import {userInput} from './pages/script';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';

function DropdownMenu() {
  return (
    <div>
        <form>
            <div>
            <label for="Region">Select a Region:  </label>
                <select id="Region">
                    <option value="Santa Barbara">Santa Barbara</option>
                    <option value="Carpinteria">Carpinteria</option>
                    <option value="Ventura">Ventura</option>
                    <option value="Oxnard">Oxnard</option>
                </select>
            </div><br></br>
            <div>
            <label for="Start">Select Start Year:  </label>
                <select id="Start">
                    <option value="2003">2003</option>
                    <option value="2004">2004</option>
                    <option value="2005">2005</option>
                    <option value="2006">2006</option>
                    <option value="2007">2007</option>
                    <option value="2008">2008</option>
                    <option value="2009">2009</option>
                    <option value="2010">2010</option>
                    <option value="2011">2011</option>
                    <option value="2012">2012</option>
                    <option value="2013">2013</option>
                    <option value="2014">2014</option>
                    <option value="2015">2015</option>
                    <option value="2016">2016</option>
                    <option value="2017">2017</option>
                </select>
            </div><br></br>
            <div>
            <label for="End">Select End Year:  </label>
                <select id="End">
                    <option value="2003">2003</option>
                    <option value="2004">2004</option>
                    <option value="2005">2005</option>
                    <option value="2006">2006</option>
                    <option value="2007">2007</option>
                    <option value="2008">2008</option>
                    <option value="2009">2009</option>
                    <option value="2010">2010</option>
                    <option value="2011">2011</option>
                    <option value="2012">2012</option>
                    <option value="2013">2013</option>
                    <option value="2014">2014</option>
                    <option value="2015">2015</option>
                    <option value="2016">2016</option>
                    <option value="2017">2017</option>
                </select>
            </div><br></br>
            <button id="btn" onClick={userInput}>Get the Selected Value</button>
            
    </form>
    
    </div>
  )
}

export default DropdownMenu

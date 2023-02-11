import React from 'react';
import '../App.css'
import { Button } from './Button';
import './FireSection.css';

function FireSection() {
  return (
    <div className='hero-container'>
        <video src="/videos/wildfire.mp4" autoPlay loop muted />
        <h1>Team Flare Wildfire Prediction Model</h1>
        <div className="hero-btns">
            <Button
            className='btns'
            buttonStyle='btn--primary'
            buttonSize='btn--exlarge'
            >
                Try Now
            </Button>
        </div>
    </div>
  );
}

export default FireSection;
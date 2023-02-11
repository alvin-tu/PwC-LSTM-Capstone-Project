import React from 'react'
import '../../App.css'
import './About.css'


const Card = ({ description, imageUrl, text }) => (
    <div className="about__card">
      <div className="about__text__container">
        <p className='about__text'>{text}</p>
      </div>
      <div className="about__image__container">
        <img className='about__image' src={imageUrl}/>
        <p className='about__image__text'>{description}</p>
      </div>
    </div>
  );

export default function About() {
    return (
    <div>
        <h1 className='about'>Using the Prediction Model</h1>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <Card description="Data" imageUrl='photos/kirby.jpeg' text="TODO: FILL IN" />
            <Card description="How to Use" imageUrl='photos/kirby.jpeg' text="TODO: FILL IN" />
            <Card description="Example Results" imageUrl='photos/kirby.jpeg' text="TODO: FILL IN" />
        </div>
    </div>
    );
}
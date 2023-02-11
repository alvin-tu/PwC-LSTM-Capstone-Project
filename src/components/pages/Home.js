import React from 'react';
import '../../App.css';
import Cards from '../Cards';
import FireSection from '../FireSection';
import './Home.css';

function Home () {
    return (
        <div>
            <FireSection />
            <div className='next'>
                <h1>Our Problem</h1>
                <div className='problem'>
                    <p>Wildfires are a serious environmental concern that cause not only economic and ecological harm, but also put human 
                        lives in danger. With growing climate change, wildfires are an increasingly dangerous problem, which makes it even 
                        more imperative to be able to predict and prepare for them. Various conditions increase the likelihood of 
                        wildfires, such as the presence of fuel or residing in a dry climate. By using these variables, we can generate 
                        predictive models that estimate the long term effects of climate change on wildfire occurrences, ultimately 
                        reducing the damage they have on the environment and society. Currently, many areas are in danger from wildfires, 
                        with few means to detect and prevent them in the long term. As climate change worsens, we need to prepare for the 
                        increased occurrences of wildfires since it will not only help reduce business risks caused from wildfires, 
                        but also potentially save lives and protect the environment. Our team will tackle this problem by using deep 
                        learning approaches to predict potential wildfires.
                    </p>
                </div>
                <div>
                    <h1>About Us</h1>
                </div>
                <div className='us'>
                    <p>We are a group of senior Computer Engineering students from the University of California, Santa Barbara.
                        Meet the team:
                    </p>
                </div>
            </div>
            <Cards />
        </div>
    );
}

export default Home;
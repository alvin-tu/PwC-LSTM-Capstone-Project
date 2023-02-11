import React from 'react';
import './Cards.css';
import CardItem from './CardItem';

function Cards() {
  return (
    <div className='cards'>
      <div className='cards__container'>
        <div className='cards__wrapper'>
          <ul className='cards__items'>
            <CardItem
              src='photos/LIN.png'
              text='Kelly Lin'
              label='Leader'
              path='https://www.linkedin.com/in/kelly-lin-7689251a0/'
            />
            <CardItem
              src='photos/TU.png'
              text='Alvin Tu'
              label='Scribe'
              path='https://www.linkedin.com/in/alvin-w-tu/'
            />
            <CardItem
              src='photos/ONG.png'
              text='Nick Ong'
              label='Member'
              path='https://www.linkedin.com/in/nick-ong/'
            />
            <CardItem
              src='photos/CHANG.png'
              text='Steven Chang'
              label='Member'
              path='https://www.linkedin.com/in/steven-chang-00368319b/'
            />
            <CardItem
              src='photos/shou.png'
              text='Shuya Shou'
              label='Member'
              path='https://www.linkedin.com/in/shuya-shou-155053265/'
            />
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Cards;
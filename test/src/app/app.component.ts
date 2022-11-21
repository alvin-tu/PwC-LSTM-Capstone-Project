import { Component } from '@angular/core';

declare function outputData():any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  template: `
  <form action="/app.component.html" method="get">
  <label for="regions">Region:</label>
  <input list="regionList"  id = "rl" name="regionList" formControlName="regionList" required/>
  <datalist id="regionList">
      <option value="NSW">
      <option value="NT">
      <option value="QL">
      <option value="SA">
      <option value="TA">
      <option value="VI">
      <option value="WA"></option>
  </datalist>
  <label for="start">Start date:</label>
  <input type="date" id="start" name="trip-start"
      value="2017-09-13"
      min="2005-01-04" max="2017-09-13">
  <label for="forecastDays"> Forecasting Range:</label>
  <input list="forecastList" id = "fl" name="forecastList"/>
  <datalist id="forecastList">
      <option value="5 days">
      <option value="1 week">
      <option value="2 weeks">
      <option value="1 month">
      <option value="6 months"></option>
  </datalist>

  <input type="submit" value="Submit">
  </form>
  `
})

export class AppComponent {
  title = 'LSTM Prediction Model';
  input1 = 'Region';
  input2 = 'Start Date';
  input3 = 'Forecasting Range'


  ngOnInit(): void{
    outputData();
  }
}

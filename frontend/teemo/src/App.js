import React, { Component } from 'react';
import './App.css';
import { Route, Switch } from 'react-router-dom';
import MainPage from './containers/MainPage.js';
import SignUpCustomerPage from './containers/SignUpCustomerPage.js';
import SignUpStorePage from './containers/SignUpStorePage.js';
import NotFoundPage from './pages/NotFoundPage.js';
import CustomerPage from './containers/CustomerPage.js';
import StorePage from './containers/StorePage.js';

class App extends Component {

  render() {
	  const Routing = () => (
		<div className="App">
			<Switch>
				<Route exact path="/" component={MainPage}/>
				<Route path="/SignUpCustomer" component={SignUpCustomerPage}/>
				<Route path="/SignUpStore" component={SignUpStorePage}/>
				<Route path="/Customer" component={CustomerPage}/>
				<Route path="/Store" component={StorePage}/>
				<Route component={NotFoundPage}/>
			</Switch>
		</div>
	  )
	
    return (
        <div className="App">

			<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
			<Routing/>
        </div>
    );
  }
}

export default App;

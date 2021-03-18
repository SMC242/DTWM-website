import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { Home } from "./pages/home";
import { NotFoundErrorPage } from "./pages/404";

const App = () => {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route component={NotFoundErrorPage} />
      </Switch>
    </Router>
  );
};

export default App;

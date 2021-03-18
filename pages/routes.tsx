import React from "react";
import { map } from "ramda";
const routes = (module.exports = require("next-routes")());

const add_route = (name: string) => (pattern: string) => (page_name: string) =>
  routes.add(name, pattern, page_name);
const route_from_args = ([name, pattern, page_name]: [
  string,
  string,
  string
]) => add_route(name)(pattern)(page_name);
const args: [string, string, string][] = [
  ["home", "/", "index"],
  ["info", "/info", "info"],
  ["join", "/join", "join"],
];

map(route_from_args, args);

export const Link = routes.Link;
const Whoopsie = () => <span>Whoopsie</span>;
export default Whoopsie;

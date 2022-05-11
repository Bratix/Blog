// Load plugins
import cash from "cash-dom";
import helper from "./helper";
import Velocity from "velocity-animate";
import * as Popper from "@popperjs/core";
import $ from 'jquery';

// Set plugins globally
window.$ = window.jQuery = $;
window.cash = cash;
window.helper = helper;
window.Velocity = Velocity;
window.Popper = Popper;

const primaryColors = require("@left4code/tw-starter/dist/js/colors");

module.exports = {
  mode: "jit",
  purge: [
    '../blogapp/templates/**/*.html',
    "../templates/**/*.html",
  ],
  darkMode: "class",
  theme: {
    borderColor: (theme) => ({
      ...theme("colors"),
      DEFAULT: primaryColors.gray["300"],
    }),
    colors: {
      ...primaryColors,
      primary: {
        ...primaryColors.primary,
        1: "#142E71",
      },
      dark: {
        ...primaryColors.dark,
        8: "#242b3c",
      },
      white: "white",
      black: "black",
      current: "current",
      transparent: "transparent",
      theme: {
        1: "#071A50",
        2: "#2D427B",
        3: "#A2AFD5",
        4: "#C6D4FD",
        5: "#D32929",
        6: "#365A74",
        7: "#D2DFEA",
        8: "#7F9EB8",
        9: "#96A5D0",
        10: "#13B176",
        11: "#11296d",
        12: "#1f377d",
        13: "#9BADE4",
        14: "#1c3271",
        15: "#F1F5F8",
        16: "#102867",
        17: "#142E71",
        18: "#172F71",
        19: "#B2BEDE",
        20: "#102765",
        21: "#3160D8",
        22: "#F78B00",
        23: "#FBC500",
        24: "#CE3131",
        25: "#E2EBF2",
        26: "#203f90",
        27: "#8DA9BE",
        28: "#607F96",
        29: "#B8F1E1",
        30: "#FFE7D9",
        31: "#DBDFF9",
        32: "#2B4286",
        33: "#8C9DCA",
        34: "#0E2561",
        35: "#E63B1F",
      },
    },
    extend: {
      fontFamily: {
        roboto: ["Roboto"],
      },
      container: {
        center: true,
      },
      maxWidth: {
        "1/4": "25%",
        "1/2": "50%",
        "3/4": "75%",
      },
      strokeWidth: {
        0.5: 0.5,
        1.5: 1.5,
        2.5: 2.5,
      },
    },
  },
  variants: {
    extend: {
      boxShadow: ["dark"],
    },
  },
};

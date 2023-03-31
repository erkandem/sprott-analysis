export const esgGoldFilename = "esg-gold.json";
export const goldFilename = "gold.json";
export const goldAndSilver = "gold-and-silver.json";
export const platinumAndPalladiumFilename = "platinum-and-palladium.json";
export const silverFilename = "silver.json";
export const uraniumFilename = "uranium.json";
export const availableProductsData = [
  {
    name: "Uranium",
    file: uraniumFilename,
  },
  {
    name: "Silver",
    file: silverFilename,
  },
  {
    name: "Gold",
    file: goldFilename,
  },
  {
    name: "ESG Gold",
    file: esgGoldFilename,
  },
  {
    name: "Platinum and Palladium",
    file: platinumAndPalladiumFilename,
  },
  {
    name: "Gold and Silver",
    file: goldAndSilver,
  },
];
export const baseUrl = "http://127.0.0.1:8080/";

export const extractSeriesForPlotlyFormat = (
  data, // JSON dump of pandas  / Result from API
  xName, // name of the x column (i.e. index)
  yName // name of the y column (i.e. target value)
) => {
  let x = [];
  let y = [];
  for (let i = 0; i < data.length; i++) {
    // in case of a ISO string which includes "T"
    // x.push(data.data[i][xName].replace("T", " ").slice(0, 10))
    x.push(new Date(data[i][xName]));
    y.push(data[i][yName]);
  }
  return {
    x: x,
    y: y,
  };
};

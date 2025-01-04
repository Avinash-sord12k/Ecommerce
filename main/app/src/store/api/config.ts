const DEV_API_ENDPOINTS = {
  getProducts: "/api/v1/product",
  login: "/api/v1/users/login",
};

const PROD_API_ENDPOINTS = {
  getProducts: "/api/v1/product",
  login: "/api/v1/users/login",
};

export const API_ENDPOINTS =
  process.env.NODE_ENV === "production"
    ? PROD_API_ENDPOINTS
    : DEV_API_ENDPOINTS;

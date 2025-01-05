const DEV_API_ENDPOINTS = {
  getProducts: "/api/v1/product",
  login: "/api/v1/users/login",
  logout: "/api/v1/users/logout",
  me: "/api/v1/users/me",
  carts: "/api/v1/cart",
  createCart: "/api/v1/cart/create",
  addItemsInCart: "/api/v1/cart/add-item",
};

const PROD_API_ENDPOINTS = {
  getProducts: "/api/v1/product",
  login: "/api/v1/users/login",
  logout: "/api/v1/users/logout",
  me: "/api/v1/users/me",
  carts: "/api/v1/cart",
  createCart: "/api/v1/cart/create",
  addItemsInCart: "/api/v1/cart/add-item",
};

export const API_ENDPOINTS = process.env.NODE_ENV === "production" ? PROD_API_ENDPOINTS : DEV_API_ENDPOINTS;

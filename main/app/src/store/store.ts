"use client";
import { persistReducer, persistStore, FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER } from "redux-persist";
import { configureStore } from "@reduxjs/toolkit";
import { productApi } from "./api/products";
import { authApi } from "./api/auth";
import cartReducer from "./slices/cart";
import storage from "redux-persist/lib/storage";
import { setupListeners } from "@reduxjs/toolkit/query";
import { cartApi } from "./api/cart";

const persistConfigCart = {
  key: "cart",
  storage,
};

const ONE_DAY = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

const persistedCartReducer = persistReducer(persistConfigCart, cartReducer);

export const store = configureStore({
  reducer: {
    [productApi.reducerPath]: productApi.reducer,
    [authApi.reducerPath]: authApi.reducer,
    [cartApi.reducerPath]: cartApi.reducer,
    cart: persistedCartReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    })
      .concat(productApi.middleware)
      .concat(authApi.middleware)
      .concat(cartApi.middleware),
});

const persistor = persistStore(store);

setTimeout(() => {
  persistor.purge();
}, ONE_DAY);

export default store;
setupListeners(store.dispatch);

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

import { SpecificProduct } from "@/app/(main)/products/[slug]/page";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export const cartSlice = createSlice({
  name: "cart",
  initialState: {
    defaultCart: {
      id: 0,
    },
  },
  reducers: {
    setDefaultCart: (state, action: PayloadAction<number>) => {
      state.defaultCart.id = action.payload;
    },
  },
});

export const { setDefaultCart } = cartSlice.actions;
export default cartSlice.reducer;

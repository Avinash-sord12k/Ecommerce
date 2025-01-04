import { SpecificProduct } from "@/app/(main)/products/[slug]/page";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export const cartSlice = createSlice({
  name: "cart",
  initialState: {
    items: [] as {
      id: number;
      product: SpecificProduct;
      quantity: number;
      addedAt: string;
    }[],
  },
  reducers: {
    addToCart: (
      state,
      action: PayloadAction<{
        product: SpecificProduct;
        quantity: number;
      }>
    ) => {
      const existingItem = state.items.find((item) => item.id === action.payload.product.id);
      if (existingItem) {
        existingItem.quantity += action.payload.quantity;
        return;
      }
      const item = {
        id: action.payload.product.id,
        product: action.payload.product,
        quantity: action.payload.quantity,
        addedAt: new Date().toISOString(),
      };
      state.items.push(item);
    },
    removeFromCart: (state, action: PayloadAction<number>) => {
      state.items = state.items.filter((item) => item.id !== action.payload);
    },
    updateQty: (state, action: PayloadAction<{ id: number; quantity: number }>) => {
      const item = state.items.find((item) => item.id === action.payload.id);
      if (item) {
        item.quantity = action.payload.quantity;
      }

      if (item?.quantity === 0) {
        state.items = state.items.filter((item) => item.id !== action.payload.id);
      }
    },
  },
});

export const { addToCart, removeFromCart, updateQty } = cartSlice.actions;
export default cartSlice.reducer;

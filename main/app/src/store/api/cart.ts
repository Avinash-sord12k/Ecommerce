// "use client";
// import { operations } from "@/schema";
// import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
// import { API_ENDPOINTS } from "./config";

// export const cartApi = createApi({
//   reducerPath: "cartApi",
//   baseQuery: fetchBaseQuery({
//     baseUrl: "",
//     // headers: {
//     //   Authorization: `Bearer ${localStorage.getItem("token")}`,
//     // },
//   }),
//   endpoints: (builder) => ({
//     getCart: builder.mutation<
//       operations["get_cart"]["responses"]["200"]["content"]["application/json"],
//       FormData
//     >({
//       query: (body: FormData) => {
//         return {
//           url: API_ENDPOINTS.login,
//           params: { set_cookie: true },
//           method: "POST",
//           body,
//         };
//       },
//     }),
//   }),
// });

// export const { useLoginMutation } = cartApi;

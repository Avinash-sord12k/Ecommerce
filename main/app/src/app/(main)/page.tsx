import ProductGroup from "@/components/pages/home/ProductGroup";
import { operations } from "@/schema";
import { API_ENDPOINTS } from "@/store/api/config";
import { headers } from "next/headers";

export interface HomePageStructure {
  id: number;
  title: string;
  description: string;
  query: operations["get_product_by_category_id_api_v1_product_get_by_category_id_get"]["parameters"]["query"];
}

export type ProductResponse =
  operations["get_product_by_category_id_api_v1_product_get_by_category_id_get"]["responses"]["200"]["content"]["application/json"];

const pageStructure: HomePageStructure[] = [
  {
    id: 1,
    title: "Curated Products",
    description: "Check out our curated products",
    query: {
      category_id: 1,
      page: 1,
      page_size: 10,
    },
  },
  {
    id: 2,
    title: "Curated Products",
    description: "Check out our curated products",
    query: {
      category_id: 1,
      page: 1,
      page_size: 10,
    },
  },
  {
    id: 3,
    title: "Curated Products",
    description: "Check out our curated products",
    query: {
      category_id: 1,
      page: 1,
      page_size: 10,
    },
  },
];

async function getProducts(
  structure: HomePageStructure
): Promise<ProductResponse> {
  const headerList = await headers();

  const url = new URL(API_ENDPOINTS.getProductsByCategory, process.env.API_URL);

  Object.entries(structure.query).forEach(([key, value]) => {
    url.searchParams.append(key, String(value));
  });

  console.log("🚀 ~ url:", url.toString());

  const products = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization:
        headerList.get("Authorization") ??
        "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJlbWFpbCI6InRlc3RlckBnbWFpbC5jb20iLCJleHAiOjE3MzQ3MjI4Njh9.mZmtNbj8hOoiz1QOcaI3MsXKiRc7OSKSbpwk0sapQno",
    },
  }).then((res) => {
    // console.log(res);
    return res.json();
  });

  return products;
}

export default async function Home() {
  const PageData = await Promise.all(
    pageStructure.map(async (structure) => {
      const products = await getProducts(structure);
      return {
        ...structure,
        products, // Merge the products with the structure
      };
    })
  );

  console.log("🚀 ~ Home ~ PageData:", PageData);

  return (
    <main>
      <section className="bg-black py-32">
        <div className=" mx-auto container w-full">
          <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-white text-center mb-3">
            Spring Collection
          </h1>
          <p className="max-w-[600px] mx-auto text-center text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
            Introducing our vibrant and stylish spring collection. Find the
            perfect outfit for the season.
          </p>
        </div>
      </section>

      {PageData?.map((data) => (
        <ProductGroup
          key={data.id}
          id={data.id}
          query={data.query}
          title={data.title}
          description={data.description}
          products={data.products}
        />
      ))}
    </main>
  );
}

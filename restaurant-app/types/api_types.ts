type APIPagination = {
    limit: number;
    page: number;
    pages: number;
    total: number;
};

type APIMetadata = {
    api_version: string;
    pagination: APIPagination;
    size: number;
    type: string;
    type_response: string;
};

export type APIResponse<T> = {
    metadata: APIMetadata;
    response: T[];
};

type User = {
    id: number;
    username: string;
};

export type Category = {
    id: number;
    name: string;
    ingredient_description?: string;
    menu_section: string;

    products?: Product[];
};

export type ProductAddons = {
    id: number;
    type: string;
    name: string;
    price: number;

    order_addons?: OrderAddons[];
};

export type Product = {
    id: number;
    name: string;
    complete_name: string;
    ingredient_description?: string;
    price: number;
    disponibility_status: boolean;

    id_category: number;
    category?: Category;

    orders?: Order[];
};

export type OrderAddons = {
    id: number;

    id_product_addons: number;
    product_addons: ProductAddons;

    id_order: number;
    order?: Order;
};

export type Order = {
    id: number;
    quantity: number;
    finished_status: boolean;
    total: number;

    id_ticket: number;
    ticket: Ticket;

    id_product: number;
    product: Product;

    order_addons: OrderAddons[];
};

export type Ticket = {
    id: number;
    uuid: string;
    ticket_number?: number;
    comments: string;
    client_name: string | null;
    total: number;
    created_at: string;
    is_paid: boolean;
    id_user: number;

    user: User;
    id_restaurant_table: number;
    restaurant_table: RestaurantTable;

    orders: Order[];
};

export type PrintTicket = {
    id: number;
    id_ticket: number;
    printed: boolean;
    print_for_pay: boolean;
    ticket: Ticket;
};

export type RestaurantTable = {
    id: number;
    number: number;

    tickets: Ticket[];
};

// creation
export type newOrder = {
    id?: number;
    quantity: number;
    id_ticket: number;
    id_product: number;
    order_addons: number[];
};

export type newTicket = {
    id?: number;
    id_restaurant_table: number;
    comments: string;
    client_name?: string;
    is_paid?: boolean;
    id_user: number;
};

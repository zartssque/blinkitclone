import tkinter as tk
from PIL import Image, ImageTk

def load_image(path):
    img = Image.open(path).resize((150, 150), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

def create_gradient_bg(canvas, width, height):
    canvas.delete("all")
    for i in range(height):
        r = max(0, min(255, 200 - i // 4))
        g = max(0, min(255, 255 - i // 4))
        b = max(0, min(255, 200 - i // 4))
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, width, i, fill=color)

class GroceryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blinkit Style Grocery App")
        self.root.state('zoomed')
        self.cart = {}
        self.discount_applied = False

        self.products = [
            {"name": "Apples", "price": 120, "desc": "Fresh Kashmiri apples (1kg)",
             "image": load_image(r"C:\Users\admin\Downloads\pngtree-fresh-apple-fruit-red-png-image_10203073.png")},
            {"name": "Milk", "price": 50, "desc": "Amul Fresh Milk (1L)",
             "image": load_image(r"C:\Users\admin\Downloads\milk-png-11554019731zzc03ngzzv.png")},
            {"name": "Bread", "price": 40, "desc": "Harvest white bread (400g)",
             "image": load_image(r"C:\Users\admin\Downloads\png-transparent-white-bread-bread-baked-goods-food-whole-grain-thumbnail.png")},
            {"name": "Bananas", "price": 60, "desc": "Ripe yellow bananas (1 dozen)",
             "image": load_image(r"C:\Users\admin\Downloads\pngtree-banana-yellow-fruit-banana-skewers-png-image_5944324.png")},
            {"name": "Tomatoes", "price": 30, "desc": "Farm fresh tomatoes (1kg)",
             "image": load_image(r"C:\Users\admin\Downloads\png-transparent-tomato-tomato-fresh-fruits-thumbnail.png")},
            {"name": "Cheese", "price": 200, "desc": "Cheddar Cheese block (500g)",
             "image": load_image(r"C:\Users\admin\Downloads\png-transparent-milk-emmental-cheese-graphy-food-fashion-cheese-block-slices-of-cheese-fashion-girl-breakfast-cheese.png")},
        ]

        self.pages = {}
        for page_name in ['home', 'cart', 'order']:
            frame = tk.Frame(root)
            frame.place(x=0, y=0, relwidth=1, relheight=1)
            canvas = tk.Canvas(frame, highlightthickness=0)
            canvas.pack(fill="both", expand=True)
            create_gradient_bg(canvas, root.winfo_screenwidth(), root.winfo_screenheight())
            self.pages[page_name] = {'frame': frame, 'canvas': canvas}

        self.build_home()
        self.build_cart()
        self.build_order()

        self.show_page('home')

    def show_page(self, name):
        self.pages[name]['frame'].tkraise()

    def build_home(self):
        canvas = self.pages['home']['canvas']
        frame = tk.Frame(canvas, bg="white")
        canvas.create_window(0, 0, anchor="nw", window=frame, width=self.root.winfo_screenwidth())

        title = tk.Label(frame, text="Blinkit Grocery Store", font=("Archivo Black", 24, "bold"), bg="white", fg="#00b207")
        title.pack(pady=20)

        content_frame = tk.Frame(frame, bg="white")
        content_frame.pack()

        grid_frame = tk.Frame(content_frame, bg="white")
        grid_frame.pack(side="left", padx=50)

        for index, product in enumerate(self.products):
            card = tk.Frame(grid_frame, bg="white", bd=1, relief="solid", width=200, height=300)
            card.grid(row=index // 3, column=index % 3, padx=20, pady=20)
            card.grid_propagate(False)

            tk.Label(card, image=product["image"], bg="white").pack()
            tk.Label(card, text=product["name"], font=("Helvetica", 12, "bold"), bg="white").pack(pady=2)
            tk.Label(card, text=product["desc"], font=("Helvetica", 9), bg="white", fg="gray").pack()
            tk.Label(card, text=f"₹{product['price']}", font=("Helvetica", 10), bg="white").pack()
            tk.Button(card, text="ADD", font=("Helvetica", 10, "bold"), bg="#00b207", fg="white", width=10,
                      command=lambda p=product: self.add_to_cart(p)).pack(pady=5)

        cart_preview_frame = tk.Frame(content_frame, bg="white", bd=2, relief="solid", width=300, height=500)
        cart_preview_frame.pack(side="right", padx=20)
        cart_preview_frame.pack_propagate(False)

        tk.Label(cart_preview_frame, text="🛒 Cart Preview", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)

        self.live_cart_frame = tk.Frame(cart_preview_frame, bg="white")
        self.live_cart_frame.pack(pady=10)

        tk.Button(cart_preview_frame, text="Go to Cart Page", font=("Helvetica", 10, "bold"), bg="#ffc0cb", fg="black",
                  command=lambda: [self.update_cart_page(), self.show_page('cart')]).pack(pady=10)

    def update_live_cart_preview(self):
        for widget in self.live_cart_frame.winfo_children():
            widget.destroy()

        for item, details in self.cart.items():
            frame = tk.Frame(self.live_cart_frame, bg="white")
            frame.pack(pady=5)
            tk.Label(frame, text=f"{item} x {details['qty']}", font=("Helvetica", 10), bg="white").pack(side="left")
            tk.Button(frame, text="Undo", font=("Helvetica", 8), bg="#ff6666", fg="white",
                      command=lambda n=item: self.remove_from_cart(n)).pack(side="left", padx=5)

    def add_to_cart(self, product):
        name = product["name"]
        if name in self.cart:
            self.cart[name]["qty"] += 1
        else:
            self.cart[name] = {"price": product["price"], "qty": 1, "image": product["image"]}
        self.discount_applied = False
        self.promo_entry.delete(0, tk.END)
        self.show_toast(f"{name} added (Qty: {self.cart[name]['qty']})")
        self.update_live_cart_preview()

    def remove_from_cart(self, name):
        if name in self.cart:
            self.cart[name]["qty"] -= 1
            if self.cart[name]["qty"] <= 0:
                del self.cart[name]
            self.discount_applied = False
            self.promo_entry.delete(0, tk.END)
            self.update_cart_page()
            self.update_live_cart_preview()
            self.show_toast(f"{name} removed")

    def build_cart(self):
        canvas = self.pages['cart']['canvas']
        frame = tk.Frame(canvas, bg="white")
        canvas.create_window(0, 0, anchor="nw", window=frame, width=self.root.winfo_screenwidth())

        self.cart_items_frame = tk.Frame(frame, bg="white")
        self.cart_items_frame.pack(pady=20)

        self.total_label = tk.Label(frame, text="", font=("Helvetica", 14, "bold"), fg="#00b207", bg="white")
        self.total_label.pack(pady=10)

        tk.Label(frame, text="Orders above ₹200 get FREE delivery!", font=("Helvetica", 12), fg="green", bg="white").pack(pady=5)

        promo_frame = tk.Frame(frame, bg="white")
        promo_frame.pack()
        self.promo_entry = tk.Entry(promo_frame, font=("Helvetica", 12), width=20)
        self.promo_entry.pack(side="left", padx=5)
        tk.Button(promo_frame, text="Apply Code", font=("Helvetica", 10), bg="#00b207", fg="white",
                  command=self.apply_coupon).pack(side="left")

        tk.Button(frame, text="Place Order", font=("Helvetica", 12, "bold"), bg="#00b207", fg="white", width=20,
                  command=lambda: self.show_page('order')).pack(pady=20)

        tk.Button(frame, text="← Back to Home", font=("Helvetica", 10, "bold"), bg="#ffc0cb", fg="black",
                  command=lambda: self.show_page('home')).pack(pady=10)

    def update_cart_page(self):
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()

        subtotal = 0
        for item, details in self.cart.items():
            frame = tk.Frame(self.cart_items_frame, bg="white")
            frame.pack(pady=5)
            tk.Label(frame, image=details["image"], bg="white").pack(side="left", padx=5)
            info = f"{item} x {details['qty']} = ₹{details['price'] * details['qty']}"
            tk.Label(frame, text=info, font=("Helvetica", 12), bg="white").pack(side="left")
            tk.Button(frame, text="Undo", font=("Helvetica", 8), bg="#ff6666", fg="white",
                      command=lambda n=item: self.remove_from_cart(n)).pack(side="left", padx=5)
            subtotal += details["price"] * details["qty"]

        total = subtotal
        details_text = f"Subtotal: ₹{subtotal}\n"

        if subtotal > 200:
            delivery_charge = 0
            details_text += "Delivery: FREE ✅\n"
        else:
            delivery_charge = 40
            details_text += "Delivery: ₹40\n"
            total += 40

        if self.discount_applied:
            discount = total * 0.10
            total -= discount
            details_text += f"10% OFF Applied: -₹{int(discount)}\n"

        details_text += f"Total Payable: ₹{int(total)}"
        self.total_label.config(text=details_text)

    def apply_coupon(self):
        code = self.promo_entry.get().strip()
        if code.lower() == "zara":
            self.discount_applied = True
            self.show_toast("Coupon Applied! 10% OFF 🎉")
        else:
            self.show_toast("Invalid Code!")
        self.update_cart_page()

    def build_order(self):
        canvas = self.pages['order']['canvas']
        frame = tk.Frame(canvas, bg="white")
        canvas.create_window(0, 0, anchor="nw", window=frame, width=self.root.winfo_screenwidth())

        tk.Label(frame, text="✅ Order Placed Successfully!", font=("Helvetica", 24, "bold"), fg="#00b207", bg="white").pack(pady=100)
        tk.Button(frame, text="Back to Home", font=("Helvetica", 12, "bold"), bg="#ffc0cb", fg="black",
                  command=lambda: self.show_page('home')).pack()

    def show_toast(self, msg):
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.geometry("200x50+1000+600")
        toast.configure(bg="#00b207")
        tk.Label(toast, text=msg, font=("Helvetica", 10, "bold"), fg="white", bg="#00b207").pack(expand=True)
        toast.after(1200, toast.destroy)

root = tk.Tk()
app = GroceryApp(root)
root.mainloop()

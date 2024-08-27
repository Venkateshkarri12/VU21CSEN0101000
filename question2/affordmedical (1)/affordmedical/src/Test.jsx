import React, { useState, useEffect } from 'react';

const categories = ["Phone", "Computer", "TV", "Earphone", "Tablet", "Charger", "Mouse", "Keypad", "Bluetooth", "Pendrive", "Remote", "Speaker", "Headset", "Laptop", "PC"];
const companies = ["AMZ", "FLP", "SNP", "MYN", "AZO"];

const ProductList = () => {
  const [selectedCategory, setSelectedCategory] = useState(categories[0]);
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      let allProducts = [];
      for (let company of companies) {
        const response = await fetch(`http://127.0.0.1:5000/products?company=${company}&category=${selectedCategory}&top=10&minPrice=1&maxPrice=10000`);
        const data = await response.json();
        allProducts = [...allProducts, ...data];
      }
      setProducts(allProducts);
    };

    fetchProducts();
  }, [selectedCategory]);

  return (
    <div style={styles.container}>
      <select
        value={selectedCategory}
        onChange={(e) => setSelectedCategory(e.target.value)}
        style={styles.select}
      >
        {categories.map((category) => (
          <option key={category} value={category}>
            {category}
          </option>
        ))}
      </select>

      <div style={styles.gridContainer}>
        {products.map((product, index) => (
          <div key={index} style={styles.card}>
            <h3>{product.productName}</h3>
            <p style={styles.price}><strong>Price:</strong> ${product.price}</p>
            <p style={styles.company}><strong>Company:</strong> {product.company}</p>
            <p style={styles.rating}><strong>Rating:</strong> {product.rating}</p>
            <p style={styles.discount}><strong>Discount:</strong> {product.discount}%</p>
            <p style={product.availability === 'yes' ? styles.inStock : styles.outOfStock}>
              <strong>{product.availability === 'yes' ? 'In Stock' : 'Out of Stock'}</strong>
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles = {
  container: {
    margin: '20px',
  },
  select: {
    padding: '10px',
    marginBottom: '20px',
    fontSize: '16px',
    borderRadius: '5px',
  },
  gridContainer: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
  },
  card: {
    border: '1px solid #ddd',
    borderRadius: '10px',
    padding: '20px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    textAlign: 'center',
    backgroundColor: '#fff',
  },
  price: {
    color: 'black',
  },
  company: {
    color: 'black',
  },
  rating: {
    color: 'black',
  },
  discount: {
    color: 'black',
  },
  inStock: {
    color: 'green',
  },
  outOfStock: {
    color: 'red',
  },
};

export default ProductList;

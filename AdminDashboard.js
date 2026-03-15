import React, { useState, useEffect } from 'react';
import { useNavigate, Routes, Route, useLocation } from 'react-router-dom';
import axios from 'axios';
import {
  LayoutDashboard, Package, ShoppingCart, LogOut,
  Plus, Edit2, Trash2, Sparkles, TrendingUp,
  AlertCircle, CheckCircle, Clock, Truck, Share2
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Lazy-import SocialMedia to keep bundle clean
import SocialMedia from './SocialMedia';

const AdminDashboard = () => {
  const navigate  = useNavigate();
  const location  = useLocation();
  const [token, setToken]       = useState(null);
  const [username, setUsername] = useState('');

  useEffect(() => {
    const savedToken    = localStorage.getItem('reyna_admin_token');
    const savedUsername = localStorage.getItem('reyna_admin_username');
    if (!savedToken) { navigate('/admin/login'); return; }
    setToken(savedToken);
    setUsername(savedUsername || 'Admin');
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('reyna_admin_token');
    localStorage.removeItem('reyna_admin_username');
    navigate('/admin/login');
  };

  const menuItems = [
    { path: '/admin/dashboard',          icon: LayoutDashboard, label: 'Dashboard', testId: 'menu-dashboard' },
    { path: '/admin/dashboard/products', icon: Package,         label: 'Productos',  testId: 'menu-products' },
    { path: '/admin/dashboard/orders',   icon: ShoppingCart,    label: 'Pedidos',    testId: 'menu-orders'   },
    { path: '/admin/dashboard/social',   icon: Share2,          label: 'Social',     testId: 'menu-social'   },
  ];

  const isActive = (path) => {
    if (path === '/admin/dashboard') return location.pathname === path;
    return location.pathname.startsWith(path);
  };

  if (!token) return null;

  return (
    <div className="min-h-screen pt-28 pb-20 bg-black" data-testid="admin-dashboard">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex flex-col lg:flex-row gap-8">

          {/* Sidebar */}
          <div className="lg:w-64 shrink-0">
            <div className="bg-white/5 rounded-[40px] border border-white/10 p-6 sticky top-28">
              <div className="text-center mb-8 pb-6 border-b border-white/10">
                <div className="w-16 h-16 bg-[#D4AF37]/20 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span className="text-2xl font-black text-[#D4AF37]">{username.charAt(0).toUpperCase()}</span>
                </div>
                <p className="text-sm font-bold">{username}</p>
                <p className="text-[8px] text-gray-600 uppercase tracking-widest mt-1">Administrador</p>
              </div>

              <nav className="space-y-2 mb-8">
                {menuItems.map(item => (
                  <button
                    key={item.path}
                    onClick={() => navigate(item.path)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all text-left ${
                      isActive(item.path)
                        ? 'bg-[#D4AF37] text-black font-black'
                        : 'text-gray-400 hover:bg-white/5 hover:text-white'
                    }`}
                    data-testid={item.testId}
                  >
                    <item.icon size={20} />
                    <span className="text-sm uppercase tracking-widest">{item.label}</span>
                  </button>
                ))}
              </nav>

              <button
                onClick={handleLogout}
                className="w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-red-500 hover:bg-red-500/10 transition-all text-left"
                data-testid="logout-button"
              >
                <LogOut size={20} />
                <span className="text-sm uppercase tracking-widest">Cerrar Sesión</span>
              </button>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1">
            <Routes>
              <Route path="/"          element={<DashboardHome token={token} />} />
              <Route path="/products"  element={<ProductsManagement token={token} />} />
              <Route path="/orders"    element={<OrdersManagement token={token} />} />
              <Route path="/social"    element={<SocialMedia />} />
            </Routes>
          </div>
        </div>
      </div>
    </div>
  );
};

// ════════════════════════════════════════════════════════════════════════════
// Dashboard Home
// ════════════════════════════════════════════════════════════════════════════
const DashboardHome = ({ token }) => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading]     = useState(true);

  useEffect(() => { fetchAnalytics(); }, []);

  const fetchAnalytics = async () => {
    try {
      const r = await axios.get(`${API}/analytics`, { headers: { Authorization: `Bearer ${token}` } });
      setAnalytics(r.data);
    } catch {}
    finally { setLoading(false); }
  };

  if (loading) return (
    <div className="flex items-center justify-center py-20">
      <div className="w-12 h-12 border-4 border-[#D4AF37] border-t-transparent rounded-full animate-spin" />
    </div>
  );

  return (
    <div data-testid="dashboard-home">
      <h1 className="text-4xl font-black italic uppercase mb-8">Dashboard <span className="text-[#D4AF37]">General</span></h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        {[
          { icon: Package,    color: '[#D4AF37]', value: analytics?.totalProducts || 0, label: 'Productos Activos',    testId: 'stat-products' },
          { icon: ShoppingCart, color: '[#FF007F]', value: analytics?.totalOrders || 0, label: 'Pedidos Totales',      testId: 'stat-orders'   },
          { icon: TrendingUp, color: 'green-500', value: `$${(analytics?.totalRevenue||0).toLocaleString()}`, label: 'Ingresos Totales', testId: 'stat-revenue' },
          { icon: Clock,      color: 'yellow-500', value: analytics?.pendingOrders || 0, label: 'Pedidos Pendientes', testId: 'stat-pending'  },
        ].map((s) => (
          <div key={s.testId} className={`bg-gradient-to-br from-${s.color}/20 to-${s.color}/5 p-6 rounded-3xl border border-${s.color}/20`} data-testid={s.testId}>
            <s.icon className={`text-${s.color} mb-4`} size={32} />
            <p className="text-3xl font-black mb-2">{s.value}</p>
            <p className="text-xs text-gray-500 uppercase tracking-widest">{s.label}</p>
          </div>
        ))}
      </div>

      {analytics?.topProducts?.length > 0 && (
        <div className="bg-white/5 rounded-[40px] border border-white/10 p-8 mb-6">
          <h2 className="text-2xl font-black uppercase mb-6">Top <span className="text-[#D4AF37]">Productos</span></h2>
          <div className="space-y-4">
            {analytics.topProducts.map((product, idx) => (
              <div key={product.id} className="flex items-center gap-4 bg-black/40 p-4 rounded-2xl">
                <div className="w-8 h-8 bg-[#D4AF37] rounded-full flex items-center justify-center font-black text-black text-sm">{idx + 1}</div>
                {product.images?.[0] && <img src={product.images[0]} className="w-16 h-16 object-cover rounded-xl" alt={product.name} />}
                <div className="flex-1">
                  <p className="font-bold">{product.name}</p>
                  <p className="text-xs text-gray-500">{product.sold || 0} vendidos · {product.views || 0} vistas</p>
                </div>
                <p className="text-[#D4AF37] font-black">${(product.price || 0).toLocaleString()}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {analytics?.lowStockProducts > 0 && (
        <div className="bg-yellow-500/10 border border-yellow-500/20 rounded-3xl p-6">
          <div className="flex items-center gap-3">
            <AlertCircle className="text-yellow-500" size={24} />
            <div>
              <p className="font-bold text-yellow-500">Alerta de Inventario</p>
              <p className="text-sm text-gray-400">{analytics.lowStockProducts} productos con stock bajo (menos de 5 unidades)</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// ════════════════════════════════════════════════════════════════════════════
// Products Management  (sin cambios respecto al original)
// ════════════════════════════════════════════════════════════════════════════
const ProductsManagement = ({ token }) => {
  const [products, setProducts]     = useState([]);
  const [loading, setLoading]       = useState(true);
  const [showForm, setShowForm]     = useState(false);
  const [editingProduct, setEditing] = useState(null);
  const [aiLoading, setAiLoading]   = useState(false);
  const [formData, setFormData]     = useState({
    name: '', description: '', price: '', salePrice: '',
    category: 'Mujer', sizes: '', colors: '', stock: '',
    images: '', video: '', tags: '', active: true
  });

  useEffect(() => { fetchProducts(); }, []);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const r = await axios.get(`${API}/products`);
      setProducts(r.data);
    } catch {} finally { setLoading(false); }
  };

  const headers = () => ({ Authorization: `Bearer ${token}` });
  const handleChange = e => {
    const v = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({ ...formData, [e.target.name]: v });
  };

  const generateDescription = async () => {
    if (!formData.name) return alert('Ingresa el nombre del producto primero');
    setAiLoading(true);
    try {
      const r = await axios.post(`${API}/ai/generate-description`, {
        productName: formData.name, category: formData.category,
        tags: formData.tags ? formData.tags.split(',').map(t=>t.trim()) : []
      }, { headers: headers() });
      setFormData({ ...formData, description: r.data.description });
    } catch { alert('Error al generar descripción'); }
    finally { setAiLoading(false); }
  };

  const generateMarketing = async () => {
    if (!formData.name) return alert('Ingresa el nombre del producto primero');
    setAiLoading(true);
    try {
      const r = await axios.post(`${API}/ai/generate-marketing`, {
        productName: formData.name, category: formData.category,
        tags: formData.tags ? formData.tags.split(',').map(t=>t.trim()) : []
      }, { headers: headers() });
      alert(`Copy de Marketing Generado:\n\n${r.data.marketingCopy}`);
    } catch { alert('Error al generar marketing'); }
    finally { setAiLoading(false); }
  };

  const handleSubmit = async e => {
    e.preventDefault();
    const productData = {
      ...formData,
      price: parseFloat(formData.price),
      salePrice: formData.salePrice ? parseFloat(formData.salePrice) : null,
      stock: parseInt(formData.stock),
      sizes:  formData.sizes  ? formData.sizes.split(',').map(s=>s.trim())  : [],
      colors: formData.colors ? formData.colors.split(',').map(c=>c.trim()) : [],
      images: formData.images ? formData.images.split(',').map(i=>i.trim()) : [],
      tags:   formData.tags   ? formData.tags.split(',').map(t=>t.trim())   : [],
    };
    try {
      if (editingProduct) await axios.put(`${API}/products/${editingProduct.id}`, productData, { headers: headers() });
      else await axios.post(`${API}/products`, productData, { headers: headers() });
      setShowForm(false); setEditing(null); resetForm(); fetchProducts();
    } catch { alert('Error al guardar el producto'); }
  };

  const handleEdit = p => {
    setEditing(p);
    setFormData({
      name: p.name, description: p.description,
      price: p.price.toString(), salePrice: p.salePrice ? p.salePrice.toString() : '',
      category: p.category,
      sizes:  p.sizes.join(', '),  colors: p.colors.join(', '),
      stock:  p.stock.toString(),  images: p.images.join(', '),
      video:  p.video || '',       tags:   p.tags.join(', '),
      active: p.active
    });
    setShowForm(true);
  };

  const handleDelete = async id => {
    if (!window.confirm('¿Eliminar este producto?')) return;
    try { await axios.delete(`${API}/products/${id}`, { headers: headers() }); fetchProducts(); }
    catch { alert('Error al eliminar'); }
  };

  const resetForm = () => setFormData({
    name:'',description:'',price:'',salePrice:'',category:'Mujer',
    sizes:'',colors:'',stock:'',images:'',video:'',tags:'',active:true
  });

  return (
    <div data-testid="products-management">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-black italic uppercase">Gestión de <span className="text-[#D4AF37]">Productos</span></h1>
        <button onClick={() => { setShowForm(!showForm); setEditing(null); resetForm(); }}
          className="flex items-center gap-2 px-6 py-3 bg-[#D4AF37] text-black font-black uppercase text-xs rounded-full hover:scale-105 transition-transform"
          data-testid="add-product-button">
          <Plus size={20} /> Nuevo Producto
        </button>
      </div>

      {showForm && (
        <div className="bg-white/5 rounded-[40px] border border-white/10 p-8 mb-8" data-testid="product-form">
          <h2 className="text-2xl font-black uppercase mb-6">{editingProduct ? 'Editar' : 'Nuevo'} Producto</h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {[
                { label:'Nombre *',    name:'name',     type:'text',   testId:'product-name'       },
                { label:'Stock *',     name:'stock',    type:'number', testId:'product-stock'      },
                { label:'Precio *',    name:'price',    type:'number', testId:'product-price'      },
                { label:'Precio Oferta', name:'salePrice',type:'number',testId:'product-sale-price'},
              ].map(f => (
                <div key={f.name}>
                  <label className="text-xs font-black uppercase text-gray-500 mb-2 block">{f.label}</label>
                  <input type={f.type} name={f.name} value={formData[f.name]} onChange={handleChange}
                    required={f.label.includes('*')} min="0" step={f.type==='number'?'0.01':undefined}
                    className="w-full bg-black border border-white/10 rounded-2xl px-6 py-4 text-sm focus:border-[#D4AF37] outline-none"
                    data-testid={f.testId} />
                </div>
              ))}
              <div>
                <label className="text-xs font-black uppercase text-gray-500 mb-2 block">Categoría *</label>
                <select name="category" value={formData.category} onChange={handleChange}
                  className="w-full bg-black border border-white/10 rounded-2xl px-6 py-4 text-sm focus:border-[#D4AF37] outline-none"
                  data-testid="product-category">
                  {['Mujer','Hombre','Niña','Niño'].map(c=><option key={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-black uppercase text-gray-500 mb-2 block">Tags</label>
                <input type="text" name="tags" value={formData.tags} onChange={handleChange}
                  placeholder="nuevo, oferta, tendencia"
                  className="w-full bg-black border border-white/10 rounded-2xl px-6 py-4 text-sm focus:border-[#D4AF37] outline-none"
                  data-testid="product-tags" />
              </div>
              <div>
                <label className="text-xs font-black uppercase text-gray-500 mb-2 block">Tallas</label>
                <input type="text" name="sizes" value={formData.sizes} onChange={handleChange} placeholder="S, M, L, XL"
                  className="w-full bg-black border border-white/10 rounded-2xl px-6 py-4 text-sm focus:border-[#D4AF37] outline-none" />
              </div>
              <div>
                <label className="text-xs font-black uppercase text-gray-500 mb-2 block">Colores</label>
                <input type="text" name="colors" value={formData.colors} onChange={handleChange} placeholder="Negro, Blanco"
                  className="w-full bg-black border border-white/10 rounded-2xl px-6 py-4 text-sm focus:border-[#D4AF37] outline-none" />
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="text-xs font-black uppercase text-gray-500">Descripción *</label>
                <button type="button" onClick={generateDescription} disabled={aiLoading}
                  className="flex items-center gap-2 px-4 py-2 bg-[#FF007F] text-white text-[8px] font-black uppercase rounded-full hover:scale-105 disabled:opacity-50"
                  data-testid="generate-description">
                  <Sparkles size={14} /> Generar con IA
                </button>
              </div>
              <textarea name="description" value={formData.description} onChange={handleChange} required rows={4}
                className="w-full bg-black border border-white/10 rounded-2xl px-6 py-4 text-sm focus:border-[#D4AF37] outline-none"
                data-testid="product-description" />
            </div>

            <div>
              <label className="text-xs font-black uppercase text-gray-500 mb-2 block">URLs de Imágenes *</label>
              <textarea name="images" value={formData.images} onChange={handleChange} required rows={2}
                placeholder="https://imagen1.jpg, https://imagen2.jpg"
                className="w-full bg-black border border-white/10 rounded-2xl px-6 py-4 text-sm focus:border-[#D4AF37] outline-none"
                data-testid="product-images" />
            </div>

            <div className="flex items-center gap-3">
              <input type="checkbox" name="active" checked={formData.active} onChange={handleChange}
                className="w-5 h-5" data-testid="product-active" />
              <label className="text-sm font-bold">Producto Activo</label>
            </div>

            <div className="flex gap-4">
              <button type="submit"
                className="flex-1 py-4 bg-[#D4AF37] text-black font-black uppercase text-sm rounded-2xl hover:scale-[1.02]"
                data-testid="save-product">
                {editingProduct ? 'Actualizar' : 'Guardar'} Producto
              </button>
              <button type="button" onClick={generateMarketing} disabled={aiLoading}
                className="px-6 py-4 bg-[#FF007F] text-white font-black uppercase text-sm rounded-2xl hover:scale-[1.02] disabled:opacity-50"
                data-testid="generate-marketing">
                <Sparkles className="inline mr-2" size={18} /> Marketing IA
              </button>
              <button type="button" onClick={() => { setShowForm(false); setEditing(null); resetForm(); }}
                className="px-6 py-4 bg-white/5 border border-white/10 font-bold uppercase text-sm rounded-2xl hover:bg-white/10">
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      {loading
        ? <div className="flex items-center justify-center py-20"><div className="w-12 h-12 border-4 border-[#D4AF37] border-t-transparent rounded-full animate-spin"/></div>
        : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="products-grid">
            {products.map(product => (
              <div key={product.id} className="bg-white/5 rounded-[30px] border border-white/10 overflow-hidden" data-testid={`product-card-${product.id}`}>
                <div className="aspect-[4/5] relative">
                  <img src={product.images[0] || 'https://via.placeholder.com/400x500'} className="w-full h-full object-cover" alt={product.name} />
                  {!product.active && (
                    <div className="absolute inset-0 bg-black/70 flex items-center justify-center">
                      <span className="text-white font-black uppercase text-sm">Inactivo</span>
                    </div>
                  )}
                </div>
                <div className="p-6">
                  <p className="text-[8px] text-gray-500 uppercase mb-1">{product.category}</p>
                  <h3 className="font-bold uppercase text-sm mb-2 truncate">{product.name}</h3>
                  <p className="text-[#D4AF37] font-black text-lg">${Number(product.price).toLocaleString()}</p>
                  <p className="text-xs text-gray-500 mt-1 mb-4">Stock: {product.stock}</p>
                  <div className="flex gap-2">
                    <button onClick={() => handleEdit(product)}
                      className="flex-1 py-2 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10"
                      data-testid={`edit-${product.id}`}><Edit2 size={16} className="inline"/></button>
                    <button onClick={() => handleDelete(product.id)}
                      className="flex-1 py-2 bg-red-500/10 border border-red-500/20 text-red-500 rounded-xl hover:bg-red-500/20"
                      data-testid={`delete-${product.id}`}><Trash2 size={16} className="inline"/></button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )
      }
      {!loading && products.length === 0 && (
        <div className="text-center py-20 bg-white/5 rounded-[40px] border border-dashed border-white/10">
          <Package className="mx-auto mb-6 text-gray-800" size={60} />
          <p className="text-gray-500 uppercase font-black text-sm">No hay productos</p>
        </div>
      )}
    </div>
  );
};

// ════════════════════════════════════════════════════════════════════════════
// Orders Management (sin cambios)
// ════════════════════════════════════════════════════════════════════════════
const OrdersManagement = ({ token }) => {
  const [orders, setOrders]     = useState([]);
  const [loading, setLoading]   = useState(true);
  const [filter, setFilter]     = useState('all');

  useEffect(() => { fetchOrders(); }, [filter]);

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const params = filter !== 'all' ? `?status=${filter}` : '';
      const r = await axios.get(`${API}/orders${params}`, { headers: { Authorization: `Bearer ${token}` } });
      setOrders(r.data);
    } catch {} finally { setLoading(false); }
  };

  const updateStatus = async (id, status) => {
    try {
      await axios.put(`${API}/orders/${id}/status`, { status }, { headers: { Authorization: `Bearer ${token}` } });
      fetchOrders();
    } catch { alert('Error al actualizar estado'); }
  };

  const statusColor = s => ({
    nuevo:      'bg-blue-500/20 text-blue-500 border-blue-500/20',
    confirmado: 'bg-yellow-500/20 text-yellow-500 border-yellow-500/20',
    enviado:    'bg-purple-500/20 text-purple-500 border-purple-500/20',
    entregado:  'bg-green-500/20 text-green-500 border-green-500/20',
    cancelado:  'bg-red-500/20 text-red-500 border-red-500/20',
  }[s] || 'bg-gray-500/20 text-gray-500');

  const statusIcon = s => ({
    nuevo: <Clock size={16}/>, confirmado: <CheckCircle size={16}/>,
    enviado: <Truck size={16}/>, entregado: <CheckCircle size={16}/>,
    cancelado: <AlertCircle size={16}/>
  }[s] || <Clock size={16}/>);

  return (
    <div data-testid="orders-management">
      <h1 className="text-4xl font-black italic uppercase mb-8">Gestión de <span className="text-[#D4AF37]">Pedidos</span></h1>

      <div className="flex gap-2 bg-white/5 p-2 rounded-full border border-white/10 mb-8 overflow-x-auto" data-testid="order-filters">
        {[
          {value:'all',label:'Todos'},{value:'nuevo',label:'Nuevos'},
          {value:'confirmado',label:'Confirmados'},{value:'enviado',label:'Enviados'},
          {value:'entregado',label:'Entregados'}
        ].map(item => (
          <button key={item.value} onClick={() => setFilter(item.value)}
            className={`px-6 py-3 rounded-full text-[9px] font-black uppercase tracking-widest whitespace-nowrap transition-all ${
              filter === item.value ? 'bg-[#D4AF37] text-black' : 'text-gray-500 hover:text-white'
            }`}
            data-testid={`filter-${item.value}`}>
            {item.label}
          </button>
        ))}
      </div>

      {loading
        ? <div className="flex items-center justify-center py-20"><div className="w-12 h-12 border-4 border-[#D4AF37] border-t-transparent rounded-full animate-spin"/></div>
        : (
          <div className="space-y-6" data-testid="orders-list">
            {orders.map(order => (
              <div key={order.id} className="bg-white/5 rounded-[30px] border border-white/10 p-6" data-testid={`order-${order.id}`}>
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
                  <div>
                    <p className="text-[#D4AF37] font-black text-xl">{order.orderNumber}</p>
                    <p className="text-sm text-gray-500">{new Date(order.createdAt).toLocaleString('es-CO')}</p>
                  </div>
                  <div className={`px-4 py-2 rounded-full border flex items-center gap-2 text-xs font-black uppercase ${statusColor(order.status)}`}>
                    {statusIcon(order.status)} {order.status}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div>
                    <p className="text-[8px] text-gray-500 uppercase mb-2">Cliente</p>
                    <p className="font-bold">{order.customerName}</p>
                    <p className="text-sm text-gray-400">{order.phone}</p>
                  </div>
                  <div>
                    <p className="text-[8px] text-gray-500 uppercase mb-2">Dirección</p>
                    <p className="text-sm">{order.address}</p>
                    <p className="text-sm text-gray-400">{order.city}, {order.department}</p>
                  </div>
                </div>

                <div className="mb-6">
                  <p className="text-[8px] text-gray-500 uppercase mb-3">Productos</p>
                  <div className="space-y-2">
                    {order.items.map((item, idx) => (
                      <div key={idx} className="flex justify-between items-center bg-black/40 p-3 rounded-xl">
                        <div>
                          <p className="font-bold text-sm">{item.productName}</p>
                          <p className="text-xs text-gray-500">
                            {item.size && `Talla: ${item.size}`} {item.color && `· Color: ${item.color}`} · Cant: {item.quantity}
                          </p>
                        </div>
                        <p className="font-black text-[#D4AF37]">${(item.price * item.quantity).toLocaleString()}</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pt-6 border-t border-white/10">
                  <div>
                    <p className="text-sm text-gray-500">Método: <span className="text-white font-bold uppercase">{order.paymentMethod}</span></p>
                    <p className="text-2xl font-black text-[#D4AF37]">Total: ${order.total.toLocaleString()}</p>
                  </div>
                  <select value={order.status} onChange={e => updateStatus(order.id, e.target.value)}
                    className="bg-black border border-white/10 rounded-xl px-4 py-2 text-sm font-bold focus:border-[#D4AF37] outline-none"
                    data-testid={`status-select-${order.id}`}>
                    {['nuevo','confirmado','enviado','entregado','cancelado'].map(s => (
                      <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
                    ))}
                  </select>
                </div>
              </div>
            ))}
          </div>
        )
      }
      {!loading && orders.length === 0 && (
        <div className="text-center py-20 bg-white/5 rounded-[40px] border border-dashed border-white/10">
          <ShoppingCart className="mx-auto mb-6 text-gray-800" size={60} />
          <p className="text-gray-500 uppercase font-black text-sm">No hay pedidos</p>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;

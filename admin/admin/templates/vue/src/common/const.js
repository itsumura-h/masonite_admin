const DEV = {
  APIHOST: 'http://localhost:8000',
  drawerWidth: 300,
  translateX: 0
}

const PROD = {
  APIHOST: window.location.origin,
  drawerWidth: 300,
  translateX: 0
}

let CONST = null
if (process.env.NODE_ENV === 'development') {
  CONST = DEV
} else if (process.env.NODE_ENV === 'production') {
  CONST = PROD
}

export default CONST

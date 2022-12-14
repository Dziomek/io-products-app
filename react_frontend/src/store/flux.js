const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			emailToConfirm: null,
			token: null,
			username: null,
			email: null,
			is_active: null
		},
		actions: {
			syncDataFromSessionStorage: () => {
				const emailToConfirm = sessionStorage.getItem("emailToConfirm")
				const token = sessionStorage.getItem("token")
				const username = sessionStorage.getItem("username")
				const email = sessionStorage.getItem("email")
				const is_active = sessionStorage.getItem("is_active")
				if(token) setStore({ token: token })
				if(username) setStore({ username: username})
				if(email) setStore({ email: email })
				if(is_active) setStore({ is_active: is_active })
				if(emailToConfirm) setStore({ emailToConfirm: emailToConfirm })
				console.log('Store loaded. Token:', token,
					'username', username,
					'email', email,
					'email to confirm', emailToConfirm,
					'is_active', is_active)
			},
			removeStoreData: () => {
				sessionStorage.removeItem("emailToConfirm")
				sessionStorage.removeItem("token")
				sessionStorage.removeItem("username")
				sessionStorage.removeItem("email")
				sessionStorage.removeItem("is_active")
				setStore({ emailToConfirm: null })
				setStore({ token: null })
				setStore({ username: null })
				setStore({ email: null })
				setStore({ is_active: null })
			},
			login: async (token, username, email, is_active) => {
				setStore({ token: token })
				setStore({ username: username })
				setStore({ email: email })
				setStore({ is_active: is_active })
				sessionStorage.removeItem("emailToConfirm")
				setStore({ emailToConfirm: null })
			},
			logout: () => {
				fetch("http://127.0.0.1:5000/logout")
					.then(response => {
						if(response.status === 200) {
							console.log('Logged out')
							sessionStorage.removeItem("token")
							sessionStorage.removeItem("username")
							sessionStorage.removeItem("email")
							sessionStorage.removeItem("is_active")
							setStore({ token: null })
							setStore({ username: null })
							setStore({ email: null })
							setStore({ is_active: null })
						}
					})
			},
			register: (email) => {
				setStore({ emailToConfirm: email })
			}
		}
	};
};

export default getState;
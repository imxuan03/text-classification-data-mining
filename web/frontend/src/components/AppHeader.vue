<template>
    <nav class="navbar navbar-expand-lg">
        <div class="navbar-brand-container d-flex justify-content-between w-100 container">
            <a href="/" class="navbar-brand">
                <h4 >GenK News Classifier</h4>
            </a>
            <div class="ms-auto navbar-nav">
                <li class="nav-item"><b>Trang chủ</b></li>
                <li class="nav-item"><b>Liên hệ</b></li>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    computed: {},
    name: "app-header",
    methods: {
    },
};
</script>

<style scoped>

.logo{
    width: 100px;
    height: auto;
}

.navbar {
    background-color: #fff;
    height: 80px;
    position: sticky;
    width: 100%;
    top: 0;
    z-index: 1030;
    box-shadow: 0 4px 4px 0 rgba(0, 0, 0, .1);
    margin-bottom: 20px;
}

.navbar-brand-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    flex-direction: row;
}

.navbar-brand {
    margin-right: 20px;
}

.navbar-nav {
    display: flex;
    list-style: none;
    padding-left: 0;
}

.nav-item {
    margin-left: 1rem;
}

.navbar-brand h4 {
    font-weight: bold;
    font-size: 1.5em; /* Tăng kích thước chữ nếu cần */
    color: #333; /* Thay đổi màu chữ */
}

</style>
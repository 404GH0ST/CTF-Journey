<!DOCTYPE html>
<html>
<head>
    <title>JAVAT</title>
    <style>
    body {
        background-color: #000;
        color: #0f0;
        font-family: monospace;
    }
    .center {
        display: flex;
        align-items: center;
        justify-content: center;
        -webkit-flex-direction: column;
        flex-direction: column;
        height: 100vh;
    }
    .form {
        margin-top: 20px;
    }
    .input-field {
        margin-bottom: 10px;
    }
    .input-field input[type="text"], .input-field input[type="password"] {
        padding: 8px;
        border: 1px solid #0f0;
        background-color: #000;
        color: #0f0;
        border-radius: 5px;
        font-family: monospace;
    }
     .button {
        display: inline-block;
        padding: 10px 20px;
        background-color: #0f0; 
        color: black; 
        text-align: center;
        text-decoration: none;
        border: none;
        border-radius: 5px;
        transition: box-shadow 0.2s, transform 0.2s;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        font-family: monospace;
    }
    .button:hover {
        text-decoration: none;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        transform: translateY(1px);
    }
    .button.disabled, .button:disabled {
        background-color: #ccc;
        color: #666;
        cursor: not-allowed;
        box-shadow: none;
        pointer-events: none;
    }
    </style>
</head>
<body>
    <div class="center">
        <h1>JAVAT - The Comeback of the jawat</h1>
        
        <h2><haxor_codename> </${sub}>!</h2>
        <#if flag?has_content>
            <p>gg banget bang ini dah flagnya : <code>${flag}</code> &#x1f389;</p>
        </#if>
        <form class="form" action="/login" method="post">
            <div class="input-field">
                <input type="text" name="username" placeholder="Username" required>
            </div>
            <div class="input-field">
                <input type="password" name="password" placeholder="Password" required>
            </div>
            <button type="submit" class="button">Login</button>
        </form>
    </div>
</body>
</html>

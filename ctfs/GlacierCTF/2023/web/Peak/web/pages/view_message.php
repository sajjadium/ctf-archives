<?php
    include_once "../includes/session.php";
    include_once "../includes/loggedon.php";
?>
<!DOCTYPE html>
<html lang="en">
    <?php 
    include_once "../includes/header.php";
    include_once "../includes/csp.php";
    ?>
    <body>
        <?php include_once "../includes/menu.php"; ?>

        <?php
        $sql = $pdo->prepare("SELECT * FROM messages WHERE id=:id");
        $sql->bindValue(':id', $_GET['id']);
        $sql->execute();
        $message = $sql->fetch();
        
        if (!$message)
        {
            $_SESSION['error'] = "This message no longer exists. Administrators will remove messages after they have been viewed.";
            header("Location: /pages/contact.php");
            return;
        }

        if($_SESSION['user']['role'] === "admin" && $message['viewed'] == "1")
        {
            header("Location: /admin/support.php");
        }

        if($_SESSION['user']['role'] !== "admin" && $message['user_id'] !== $_SESSION['user']['id'])
        {
            $_SESSION['error'] = "You cannot access this message!";
            header("Location: /pages/contact.php");
        }
        ?>
        
        <header class="hero bg-primary text-white text-center py-5">
            <div class="container">
                <h1>Support request</h1>
            </div>
        </header>

        <section id="message" class="py-5">
            <div class="container mt-5">
                <?php if (isset($message)): ?>
                    <h1><?php echo htmlentities($message['title']);?></h1>
                    <p><?php echo $message['content']; ?>
                    <?php if($message['file'] !== "") : ?>
                        <div>
                        <img name="image" src="<?php echo $message['file']?>">
                        </div>
                    <?php endif;?>
                <?php endif; ?></p>
            </div>
        </section>
        <?php
        if($_SESSION['user']['role'] === "admin")
        {
            $sql = $pdo->prepare("UPDATE messages SET viewed = 1 WHERE id=:id");
            $sql->bindValue(':id', $message['id']);
            $sql->execute();

            $sql = $pdo->prepare("DELETE FROM messages WHERE viewed = 1 AND created_at < datetime('now', '-1 minute')");
            $sql->execute();
        }
        ?>
</body>
<?php include "../includes/footer.php"?>
</html>

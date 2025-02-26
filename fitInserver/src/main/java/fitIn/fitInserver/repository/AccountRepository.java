package fitIn.fitInserver.repository;


import fitIn.fitInserver.domain.Account;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import java.util.List;

@Repository
@RequiredArgsConstructor
public class AccountRepository {

    private final EntityManager em;


    public void save(Account account) {
        em.persist(account);
    }

    public Account findOne(Long id){
        return em.find(Account.class, id);
    }

    public List<Account> findAll(){
        return em.createQuery("select a from Account a", Account.class).getResultList();
    }

    public List<Account> findByEmail(String email){
        return em.createQuery("select a from Account a where a.email = :email", Account.class) // 특정 이름의 회원을 찾음
                .setParameter("email",email)
                .getResultList();
    }
}
